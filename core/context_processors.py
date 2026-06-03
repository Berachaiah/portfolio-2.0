from .models import ContactMessage

def unread_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {'unread_count': ContactMessage.objects.filter(is_read=False).count()}
    return {'unread_count': 0}
