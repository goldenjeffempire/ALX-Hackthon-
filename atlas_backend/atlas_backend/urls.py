"""
URL configuration for atlas_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from two_factor.urls import urlpatterns as tf_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('main.urls')),
    path('api/user/', include('user_management.urls')),
    path('api/bookings/', include('workspace_booking.urls')),
    path('api/rooms/', include('workspace_management.urls')),
    path('api/feedback/', include('feedback.urls')),
    #path('api/mobile-accessibility/', include('mobile_accessibility.urls')),
    #path('api/search/', include('search_filtering.urls')),
    path('api/integrations/', include('integrations.urls')),
    path('api/multi-tenant/', include('multi_tenant.urls')),
    path('api/security/', include('security.urls')),
    path('api/collaboration/', include('collaboration.urls')),
    path('api/localization/', include('localization.urls')),
    path('api/notifications/', include('notifications.urls')),
    #path('api/customization/', include('customization.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/reports/', include('reporting_analytics.urls')),
    path('account/', include(tf_urls)),
]
