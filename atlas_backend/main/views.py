from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SocialMediaLink, Blog, FAQ
from .serializers import SocialMediaLinkSerializer, BlogSerializer, FAQSerializer
from user_management.models import User

# API for Social Media Links
class SocialMediaLinkListView(APIView):
    def get(self, request):
        social_links = SocialMediaLink.objects.all()
        serializer = SocialMediaLinkSerializer(social_links, many=True)
        return Response(serializer.data)

# API for Blogs
class BlogListView(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

# API for FAQs
class FAQListView(APIView):
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)
