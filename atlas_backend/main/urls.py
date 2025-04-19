from django.urls import path
from . import views

urlpatterns = [
    path('social-media-links/', views.SocialMediaLinkListView.as_view(), name='social_media_links'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('faq/', views.FAQListView.as_view(), name='faq_list'),
]
