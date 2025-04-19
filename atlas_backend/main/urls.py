from django.urls import path
from . import views

urlpatterns = [
    path('hero/', views.HeroView.as_view(), name='hero'),
    path('section/<str:section_name>/', views.StaticSectionView.as_view(), name='static-section'),
    path('resources/', views.ResourceListView.as_view(), name='resources'),
    path('integrations/', views.IntegrationListView.as_view(), name='integrations'),
    path('social-media-links/', views.SocialMediaLinkListView.as_view(), name='social_media_links'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('faq/', views.FAQListView.as_view(), name='faq_list'),
]
