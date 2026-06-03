from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Certificate, StackCategory, ResearchItem, SiteSettings, Project


class Command(BaseCommand):
    help = 'Seeds the database with default portfolio content'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Site settings
        s, _ = SiteSettings.objects.get_or_create(pk=1)
        if not s.hero_headline or s.hero_headline == '':
            s.hero_headline = "Building Intelligent Systems That Move the World Forward"
            s.availability_status = True
            s.availability_label = "Open to Opportunities"
            s.save()

        # Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'berachaiah.abolaji@gmail.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('  Created superuser: admin / admin123'))
        else:
            self.stdout.write('  Superuser already exists')

        # Certificates
        certs = [
            (0,  "Diploma in AI Fundamentals",                "Alison", "Oct 2025"),
            (1,  "Diploma in Legal Studies",                  "Alison", "Sep 2025"),
            (2,  "Certified Associate in Project Management", "Alison", "May 2025"),
            (3,  "Data Analysis using Microsoft Excel",       "Alison", "May 2025"),
            (4,  "Diploma in C# Programming",                 "Alison", "Sep 2023"),
            (5,  "Power Automate for Beginners",              "Alison", "Aug 2023"),
            (6,  "Certificate in Data Analytics",             "NIIT",   "Apr 2023"),
            (7,  "How to Become a Cloud Architect",           "Alison", "Jan 2023"),
            (8,  "Data, Databases and Mining",                "Alison", "Dec 2022"),
            (9,  "Intro to Data Analytics with Python",       "Alison", "Aug 2022"),
            (10, "Introduction to R Programming",             "Alison", "Aug 2022"),
        ]
        created = 0
        for order, name, issuer, date in certs:
            _, c = Certificate.objects.get_or_create(
                name=name,
                defaults={'issuer': issuer, 'date': date, 'order': order}
            )
            if c:
                created += 1
        self.stdout.write(f'  Certificates: {created} created, {len(certs)-created} already existed')

        # Stack categories
        stacks = [
            (0,  False, "Languages",          "Python, PHP 8.2, JavaScript, SQL, R, Rust (learning), HTML/CSS, Bash"),
            (1,  False, "Backend Frameworks", "Django 6, Laravel 12, Flask, REST API, Passenger WSGI"),
            (2,  False, "AI / ML",            "Scikit-Learn, XGBoost, CNN, FAISS, sentence-transformers, HuggingFace, Groq, Llama 4, Pandas, NumPy"),
            (3,  True,  "Web3 / Blockchain",  "Alchemy API, EVM (20+ networks), Ethereum / Sepolia, Smart Contract Interaction, Soroban / Stellar, DeFi Analytics, On-Chain Data Parsing, Phishing Detection"),
            (4,  False, "Security & Auditing","Smart Contract Auditing, Code4rena, Flash Loan Analysis, Liquidation Logic, Oracle Safety, Manual Code Review, CSRF, Auth Systems"),
            (5,  False, "Data & Visualisation","Matplotlib, Seaborn, Plotly, Power BI, Canvas API, Feature Engineering, EDA, openpyxl"),
            (6,  True,  "APIs & Integrations","Google Safe Browsing API, Paystack API, MetaMask Phishing Detector, SMTP / Mailtrap, NLTK, OpenCV, Twitter API, Alchemy"),
            (7,  False, "DevOps & Deployment","cPanel / Passenger WSGI, Docker, Railway, Git / GitHub, MySQL, SQLite, PostgreSQL, Jupyter Lab, VS Code"),
            (8,  False, "Frontend",           "HTML / CSS, JavaScript, Django Templates, Jinja2, Canvas API, Responsive Design"),
            (9,  False, "Business & Domain",  "Medical AI, AgriTech, Political Analytics, Web3 / DeFi, Institutional Systems, Business Analysis, Project Management"),
        ]
        created = 0
        for order, wide, title, items in stacks:
            _, c = StackCategory.objects.get_or_create(
                title=title,
                defaults={'items': items, 'order': order, 'is_wide': wide}
            )
            if c:
                created += 1
        self.stdout.write(f'  Stack categories: {created} created, {len(stacks)-created} already existed')

        # Research items
        research = [
            (1, "🧠 Early Alzheimer's Detection via MRI",
             "CNN-based classifier trained on MRI data to detect early-stage Alzheimer's with high accuracy. Bridges clinical decision support and ML innovation using Python, Scikit-Learn, and medical imaging datasets."),
            (2, "🗳️ Nigerian Election Sentiment Analysis",
             "NLP pipeline analysing social media sentiment to model election trends using Python, NLTK, Twitter API, and ML classifiers — a novel application of political NLP to African democracies."),
            (3, "🛒 Dataset Marketplace Platform",
             "A marketplace where curated datasets can be discovered, shared, and exchanged — advancing open data ecosystems for AI research communities. Built with Python, database engineering, and API design."),
            (4, "🔐 DeFi Smart Contract Security Research",
             "Manual code review and vulnerability analysis of DeFi lending protocols on Soroban/Stellar. Confirmed Medium severity finding on K2 — systematic protocol fee undercollection in swap collateral mechanics on Code4rena."),
        ]
        created = 0
        for num, title, desc in research:
            _, c = ResearchItem.objects.get_or_create(
                number=num,
                defaults={'title': title, 'description': desc}
            )
            if c:
                created += 1
        self.stdout.write(f'  Research items: {created} created, {len(research)-created} already existed')

        # Projects
        projects = [
            {
                'title': 'NeuroChain — AI-Powered Web3 Wallet Analytics Platform',
                'subtitle': 'Django 6 · Alchemy API · FAISS · 20+ EVM Networks',
                'description': 'Comprehensive blockchain analytics across 20+ EVM networks. ML-powered risk scoring (0–100, 6-axis radar chart), live phishing detection (17,000+ domains + Google Safe Browsing API), transaction explainer, whale alert detection, cross-chain portfolio tracker, DeFi LP calculator. Full auth + Paystack/ETH crypto payments.',
                'status': 'active', 'is_featured': True, 'order': 0,
                'stack_tags': 'Django 6, Alchemy API, FAISS, sentence-transformers, Paystack API, Canvas API, 20+ EVM Networks',
            },
            {
                'title': 'Supreme Court of Nigeria — Staff LMS',
                'subtitle': 'Django 6 · Groq / Llama 4 · MySQL · cPanel',
                'description': 'Full LMS for Supreme Court staff — training calendar, AI course builder (Llama 4), e-learning wizard, onboarding assessments with AI-generated quizzes, role-based access control, deployed on shared hosting.',
                'status': 'live', 'is_featured': False, 'order': 1,
                'stack_tags': 'Django 6, Groq / Llama 4, MySQL, RBAC, cPanel',
            },
            {
                'title': 'The Honest Friend — LLM Behavioural AI Agent',
                'subtitle': 'DSN × BCT Hackathon 3.0 · May 2026',
                'description': 'Agentic AI that builds a behavioural persona from review history and recommends experiences like a trusted Nigerian friend — honest, opinionated, culturally aware. Cross-domain across Yelp, Amazon, Goodreads. Hit Rate@10: 31× random baseline.',
                'status': 'hackathon', 'is_featured': False, 'order': 2,
                'stack_tags': 'Llama Scout 4, FAISS, Flask, Nigerian cultural NLP, sentence-transformers',
            },
            {
                'title': 'Smart Contract Security Audit — K2 DeFi Protocol',
                'subtitle': 'Code4rena · Soroban / Stellar · Rust',
                'description': 'Competitive smart contract audit on Code4rena. Audited K2, a DeFi lending protocol on Stellar\'s Soroban platform — flash loan mechanics, liquidation logic, oracle safety, swap collateral flows. Identified and submitted a confirmed Medium severity vulnerability involving systematic protocol fee undercollection.',
                'status': 'audit', 'is_featured': False, 'order': 3,
                'stack_tags': 'Rust, Soroban, Stellar, DeFi / Lending, Code4rena, Manual Review',
            },
            {
                'title': 'Memorial Tribute Site',
                'subtitle': 'Django · Groq / Llama · SMTP · openpyxl',
                'description': 'Digital memorial allowing family worldwide to submit tributes. Groq-powered AI polishing with Yoruba diacritic preservation, SMTP email confirmation, Excel export archiving, carousel tribute display.',
                'status': 'live', 'is_featured': False, 'order': 4,
                'stack_tags': 'Groq / Llama, Django, SMTP, Yoruba NLP, openpyxl',
            },
            {
                'title': 'Laravel 12 School Management REST API',
                'subtitle': 'Laravel 12 · PHP 8.2 · MySQL · REST',
                'description': 'Clean RESTful backend for a school management system — student, tutor, and parent controllers with full CRUD, proper relational design, API auth. Built to serve multiple frontends and mobile apps.',
                'status': 'active', 'is_featured': False, 'order': 5,
                'stack_tags': 'Laravel 12, PHP 8.2, MySQL, REST API',
            },
        ]
        created = 0
        for p in projects:
            _, c = Project.objects.get_or_create(
                title=p['title'],
                defaults={k: v for k, v in p.items() if k != 'title'}
            )
            if c:
                created += 1
        self.stdout.write(f'  Projects: {created} created, {len(projects)-created} already existed')

        self.stdout.write(self.style.SUCCESS('\nDone! Database seeded successfully.'))
        self.stdout.write(self.style.WARNING('Login: admin / admin123  — change this password!'))
