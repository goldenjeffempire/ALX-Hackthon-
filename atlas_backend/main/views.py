from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SocialMediaLink, Blog, FAQ, HeroContent, StaticSection, Resource, Integration
from .serializers import SocialMediaLinkSerializer, BlogSerializer, FAQSerializer, HeroContentSerializer, StaticSectionSerializer, ResourceSerializer, IntegrationSerializer
from user_management.models import User

class HeroView(APIView):
    def get(self, request):
        hero = HeroContent.objects.first()
        serializer = HeroContentSerializer(hero)
        return Response(serializer.data)

class StaticSectionView(APIView):
    def get(self, request, section_name):
        try:
            section = StaticSection.objects.get(section_name=section_name)
            serializer = StaticSectionSerializer(section)
            return Response(serializer.data)
        except StaticSection.DoesNotExist:
            return Response({"error": "Section not found"}, status=404)

class ResourceListView(APIView):
    def get(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)

class IntegrationListView(APIView):
    def get(self, request):
        integrations = Integration.objects.all()
        serializer = IntegrationSerializer(integrations, many=True)
        return Response(serializer.data)

class SocialMediaLinkListView(APIView):
    def get(self, request):
        social_links = SocialMediaLink.objects.all()
        serializer = SocialMediaLinkSerializer(social_links, many=True)
        return Response(serializer.data)

class BlogListView(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

class FAQListView(APIView):
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)
