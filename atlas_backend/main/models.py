from django.db import models

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
