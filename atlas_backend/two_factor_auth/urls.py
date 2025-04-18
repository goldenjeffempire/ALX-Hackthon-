# two_factor_auth/urls.py
from django.urls import path
from . import views

app_name = 'two_factor_auth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('setup/', views.setup_view, name='setup'),
    path('qrcode/', views.qr_code_view, name='qr'),
    path('setup/complete/', views.setup_complete_view, name='setup_complete'),
    path('backup/tokens/', views.backup_tokens_view, name='backup_tokens'),
    path('disable/', views.disable_view, name='disable'),
]
