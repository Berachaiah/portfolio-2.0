import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings
from .models import (SiteSettings, HeroImage, Project, ResearchItem,
                     Certificate, StackCategory, ContactMessage)


# ── Public portfolio ────────────────────────────────────────────────

def index(request):
    site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
    hero_images = HeroImage.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True)
    research = ResearchItem.objects.filter(is_active=True)
    certificates = Certificate.objects.filter(is_active=True)
    stacks = StackCategory.objects.filter(is_active=True)
    return render(request, 'core/index.html', {
        'settings': site_settings,
        'hero_images': hero_images,
        'projects': projects,
        'research': research,
        'certificates': certificates,
        'stacks': stacks,
    })


@require_POST
def contact_submit(request):
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    engagement_type = request.POST.get('type', '').strip()
    message_text = request.POST.get('message', '').strip()
    if not (name and email and message_text):
        return JsonResponse({'status': 'error', 'msg': 'Missing fields'}, status=400)

    ContactMessage.objects.create(
        name=name, email=email,
        engagement_type=engagement_type, message=message_text
    )

    # Send notification email
    try:
        subject = f"New portfolio enquiry from {name}"
        body = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Type: {engagement_type or 'Not specified'}\n\n"
            f"Message:\n{message_text}\n\n"
            f"---\nReply directly to: {email}"
        )
        send_mail(
            subject=subject,
            message=body,
            from_email=django_settings.DEFAULT_FROM_EMAIL,
            recipient_list=[django_settings.CONTACT_NOTIFY_EMAIL],
            fail_silently=True,
            reply_to=[email],
        )
    except Exception:
        pass  # Don't break the form if email fails

    return JsonResponse({'status': 'ok'})


# ── Admin dashboard ─────────────────────────────────────────────────

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'admin_dash/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required(login_url='/admin-panel/login/')
def admin_dashboard(request):
    ctx = {
        'projects_count': Project.objects.count(),
        'messages_count': ContactMessage.objects.filter(is_read=False).count(),
        'certs_count': Certificate.objects.count(),
        'projects': Project.objects.all()[:5],
        'recent_messages': ContactMessage.objects.all()[:5],
    }
    return render(request, 'admin_dash/dashboard.html', ctx)


@login_required(login_url='/admin-panel/login/')
def admin_settings(request):
    site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
    if request.method == 'POST':
        site_settings.hero_headline = request.POST.get('hero_headline', site_settings.hero_headline)
        site_settings.hero_sub = request.POST.get('hero_sub', site_settings.hero_sub)
        site_settings.about_text = request.POST.get('about_text', site_settings.about_text)
        site_settings.availability_label = request.POST.get('availability_label', site_settings.availability_label)
        site_settings.availability_status = 'availability_status' in request.POST
        if 'portrait' in request.FILES:
            site_settings.portrait = request.FILES['portrait']
        site_settings.save()
        messages.success(request, 'Settings saved.')
        return redirect('admin_settings')
    return render(request, 'admin_dash/settings.html', {'settings': site_settings})


@login_required(login_url='/admin-panel/login/')
def admin_hero_images(request):
    if request.method == 'POST':
        caption = request.POST.get('caption', '')
        order = request.POST.get('order', 0)
        if 'image' in request.FILES:
            HeroImage.objects.create(image=request.FILES['image'], caption=caption, order=order)
            messages.success(request, 'Hero image added.')
        return redirect('admin_hero_images')
    imgs = HeroImage.objects.all()
    return render(request, 'admin_dash/hero_images.html', {'images': imgs})


@login_required(login_url='/admin-panel/login/')
def admin_hero_image_delete(request, pk):
    get_object_or_404(HeroImage, pk=pk).delete()
    messages.success(request, 'Image deleted.')
    return redirect('admin_hero_images')


@login_required(login_url='/admin-panel/login/')
def admin_projects(request):
    projects = Project.objects.all()
    return render(request, 'admin_dash/projects.html', {'projects': projects})


@login_required(login_url='/admin-panel/login/')
def admin_project_edit(request, pk=None):
    project = get_object_or_404(Project, pk=pk) if pk else None
    if request.method == 'POST':
        data = request.POST
        if not project:
            project = Project()
        project.title = data.get('title', '')
        project.subtitle = data.get('subtitle', '')
        project.description = data.get('description', '')
        project.tag = data.get('tag', '')
        project.status = data.get('status', 'completed')
        project.stack_tags = data.get('stack_tags', '')
        project.is_featured = 'is_featured' in data
        project.order = int(data.get('order', 0))
        project.is_active = 'is_active' in data
        if 'image' in request.FILES:
            project.image = request.FILES['image']
        project.save()
        messages.success(request, 'Project saved.')
        return redirect('admin_projects')
    return render(request, 'admin_dash/project_edit.html', {'project': project})


@login_required(login_url='/admin-panel/login/')
def admin_project_delete(request, pk):
    get_object_or_404(Project, pk=pk).delete()
    messages.success(request, 'Project deleted.')
    return redirect('admin_projects')


@login_required(login_url='/admin-panel/login/')
def admin_certificates(request):
    if request.method == 'POST':
        Certificate.objects.create(
            name=request.POST.get('name', ''),
            issuer=request.POST.get('issuer', ''),
            date=request.POST.get('date', ''),
            order=int(request.POST.get('order', 0)),
        )
        messages.success(request, 'Certificate added.')
        return redirect('admin_certificates')
    certs = Certificate.objects.all()
    return render(request, 'admin_dash/certificates.html', {'certs': certs})


@login_required(login_url='/admin-panel/login/')
def admin_cert_edit(request, pk):
    cert = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        cert.name = request.POST.get('name', cert.name)
        cert.issuer = request.POST.get('issuer', cert.issuer)
        cert.date = request.POST.get('date', cert.date)
        cert.order = int(request.POST.get('order', cert.order))
        cert.save()
        messages.success(request, 'Certificate updated.')
        return redirect('admin_certificates')
    return render(request, 'admin_dash/cert_edit.html', {'cert': cert})


@login_required(login_url='/admin-panel/login/')
def admin_cert_delete(request, pk):
    get_object_or_404(Certificate, pk=pk).delete()
    messages.success(request, 'Certificate deleted.')
    return redirect('admin_certificates')


@login_required(login_url='/admin-panel/login/')
def admin_stacks(request):
    if request.method == 'POST':
        StackCategory.objects.create(
            title=request.POST.get('title', ''),
            items=request.POST.get('items', ''),
            order=int(request.POST.get('order', 0)),
            is_wide='is_wide' in request.POST,
        )
        messages.success(request, 'Stack category added.')
        return redirect('admin_stacks')
    stacks = StackCategory.objects.all()
    return render(request, 'admin_dash/stacks.html', {'stacks': stacks})


@login_required(login_url='/admin-panel/login/')
def admin_stack_edit(request, pk):
    stack = get_object_or_404(StackCategory, pk=pk)
    if request.method == 'POST':
        stack.title = request.POST.get('title', stack.title)
        stack.items = request.POST.get('items', stack.items)
        stack.order = int(request.POST.get('order', stack.order))
        stack.is_wide = 'is_wide' in request.POST
        stack.is_active = 'is_active' in request.POST
        stack.save()
        messages.success(request, 'Stack category updated.')
        return redirect('admin_stacks')
    return render(request, 'admin_dash/stack_edit.html', {'stack': stack})


@login_required(login_url='/admin-panel/login/')
def admin_stack_delete(request, pk):
    get_object_or_404(StackCategory, pk=pk).delete()
    return redirect('admin_stacks')


@login_required(login_url='/admin-panel/login/')
def admin_messages_view(request):
    msgs = ContactMessage.objects.all()
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    return render(request, 'admin_dash/messages.html', {'messages': msgs})


@login_required(login_url='/admin-panel/login/')
def admin_research(request):
    if request.method == 'POST':
        ResearchItem.objects.create(
            number=int(request.POST.get('number', 1)),
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
        )
        messages.success(request, 'Research item added.')
        return redirect('admin_research')
    items = ResearchItem.objects.all()
    return render(request, 'admin_dash/research.html', {'items': items})


@login_required(login_url='/admin-panel/login/')
def admin_research_edit(request, pk):
    item = get_object_or_404(ResearchItem, pk=pk)
    if request.method == 'POST':
        item.number = int(request.POST.get('number', item.number))
        item.title = request.POST.get('title', item.title)
        item.description = request.POST.get('description', item.description)
        item.save()
        messages.success(request, 'Research item updated.')
        return redirect('admin_research')
    return render(request, 'admin_dash/research_edit.html', {'item': item})


@login_required(login_url='/admin-panel/login/')
def admin_research_delete(request, pk):
    get_object_or_404(ResearchItem, pk=pk).delete()
    return redirect('admin_research')


# ── AI Chat proxy (dev: calls Groq directly; prod: Netlify function handles it) ─
@csrf_exempt
@require_POST
def ai_chat(request):
    import json, urllib.request, urllib.error
    try:
        body = json.loads(request.body)
        message = body.get('message', '').strip()
        history = body.get('history', [])
        if not message:
            return JsonResponse({'reply': 'Say something!'})
    except Exception:
        return JsonResponse({'reply': 'Invalid request.'}, status=400)

    groq_key = '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'
    print(f"DEBUG key: {repr(groq_key[:20])}")
    print(f"DEBUG message: {repr(message)}")
    if not groq_key:
        return JsonResponse({'reply': 'AI not configured yet — email berachaiah.abolaji@gmail.com!'})

    AI_SYSTEM = """You are The Best AI — an assistant on Berachaiah Abolaji's portfolio.
Answer questions about him concisely (under 100 words), enthusiastically and warmly.
Berachaiah is a Full-Stack Developer, AI/ML Engineer, Web3 Builder & Security Researcher based in Abuja, Nigeria.
Key projects: NeuroChain (AI Web3 analytics, 20+ EVM), SCN Staff LMS (Supreme Court), The Honest Friend (hackathon, ₦4M pool), K2 DeFi audit (Code4rena, confirmed Medium severity), Memorial Tribute Site, Laravel 12 School API.
Skills: Python 92%, Django 6, Laravel 12, FAISS, XGBoost, CNN, Groq/Llama, Alchemy API, Soroban/Stellar.
Open to freelance, contracts, full-time roles. Contact: berachaiah.abolaji@gmail.com"""

    messages = [{'role': 'system', 'content': AI_SYSTEM}]
    messages += history[-8:]
    messages.append({'role': 'user', 'content': message})

    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': messages,
        'max_tokens': 200,
        'temperature': 0.7,
    }).encode()

    req = urllib.request.Request(
        'https://api.groq.com/openai/v1/chat/completions',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {groq_key}',
            'User-Agent': 'Mozilla/5.0',
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            reply = data['choices'][0]['message']['content']
            return JsonResponse({'reply': reply})
    except Exception as e:
        print(f"DEBUG GROQ ERROR: {repr(e)}")
        import traceback; traceback.print_exc()
        return JsonResponse({'reply': 'AI is temporarily offline — email berachaiah.abolaji@gmail.com!'})