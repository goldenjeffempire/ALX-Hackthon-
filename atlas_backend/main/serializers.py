from rest_framework import serializers
from .models import SocialMediaLink, Blog, FAQ, HeroContent, StaticSection, Resource, Integration

class HeroContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroContent
        fields = '__all__'

class StaticSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSection
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = '__all__'

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
