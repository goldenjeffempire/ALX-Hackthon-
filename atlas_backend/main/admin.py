# main/admin.py
from django.contrib import admin
from .models import HeroContent, StaticSection, Resource, Integration, SocialMediaLink, Blog, FAQ

admin.site.register(HeroContent)
admin.site.register(StaticSection)
admin.site.register(Resource)
admin.site.register(Integration)
admin.site.register(FAQ)
admin.site.register(Blog)
admin.site.register(SocialMediaLink)
