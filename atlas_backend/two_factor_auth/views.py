# two_factor_auth/views.py
from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return HttpResponse("Login view")

def setup_view(request):
    return HttpResponse("Setup view")

def qr_code_view(request):
    return HttpResponse("QR Code view")

def setup_complete_view(request):
    return HttpResponse("Setup complete view")

def backup_tokens_view(request):
    return HttpResponse("Backup tokens view")

def disable_view(request):
    return HttpResponse("Disable view")
