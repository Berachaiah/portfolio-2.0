from django.db import models


class SiteSettings(models.Model):
    hero_headline = models.CharField(max_length=200, default="Building Intelligent Systems That Move the World Forward")
    hero_sub = models.TextField(default="")
    hero_cta_primary = models.CharField(max_length=60, default="Hire Me Now")
    hero_cta_secondary = models.CharField(max_length=60, default="View Projects")
    portrait = models.ImageField(upload_to='portraits/', blank=True, null=True)
    about_text = models.TextField(default="")
    availability_status = models.BooleanField(default=True)
    availability_label = models.CharField(max_length=100, default="Open to Opportunities")

    class Meta:
        verbose_name = "Site Settings"

    def __str__(self):
        return "Site Settings"


class HeroImage(models.Model):
    image = models.ImageField(upload_to='hero/')
    caption = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Hero Image {self.order}"


class Project(models.Model):
    STATUS_CHOICES = [
        ('live', 'Live'),
        ('active', 'Active Development'),
        ('completed', 'Completed'),
        ('hackathon', 'Hackathon'),
        ('audit', 'Security Audit'),
    ]
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    tag = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    stack_tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def stack_list(self):
        return [s.strip() for s in self.stack_tags.split(',') if s.strip()]


class ResearchItem(models.Model):
    number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.title


class Certificate(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=100)
    date = models.CharField(max_length=30)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} — {self.issuer}"


class StackCategory(models.Model):
    title = models.CharField(max_length=80)
    items = models.TextField(help_text="Comma-separated list")
    order = models.PositiveIntegerField(default=0)
    is_wide = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Stack Categories"

    def __str__(self):
        return self.title

    def item_list(self):
        return [s.strip() for s in self.items.split(',') if s.strip()]


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    engagement_type = models.CharField(max_length=80, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.created_at.strftime('%d %b %Y')}"
