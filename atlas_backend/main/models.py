from django.db import models


class HeroContent(models.Model):
    heading = models.CharField(max_length=255)
    subheading = models.TextField()
    description = models.TextField()
    demo_button_text = models.CharField(max_length=100)
    pricing_button_text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hero/')

class StaticSection(models.Model):
    SECTION_CHOICES = (
        ('about', 'About'),
        ('pricing', 'Pricing'),
    )
    section_name = models.CharField(max_length=50, choices=SECTION_CHOICES, unique=True)
    heading = models.CharField(max_length=255)
    description = models.TextField()

class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='resources/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class Integration(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100)

class SocialMediaLink(models.Model):
    platform = models.CharField(max_length=50)  # e.g., 'LinkedIn', 'Instagram', 'Twitter'
    url = models.URLField()

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
