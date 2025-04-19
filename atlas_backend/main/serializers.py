from rest_framework import serializers
from .models import SocialMediaLink, Blog, FAQ

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url']

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'created_at']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
