from django.contrib import admin
from .models import SiteSettings, HeroImage, Project, ResearchItem, Certificate, StackCategory, ContactMessage

admin.site.register(SiteSettings)
admin.site.register(HeroImage)
admin.site.register(Project)
admin.site.register(ResearchItem)
admin.site.register(Certificate)
admin.site.register(StackCategory)
admin.site.register(ContactMessage)
