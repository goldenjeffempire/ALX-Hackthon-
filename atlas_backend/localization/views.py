# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserTimezone
from django.utils import timezone
from .forms import TimezoneForm, LanguageForm
from django.conf import settings

def update_timezone(request):
    if request.method == 'POST':
        form = TimezoneForm(request.POST)
        if form.is_valid():
            timezone_str = form.cleaned_data['timezone']
            # Update user's timezone
            UserTimezone.objects.update_or_create(user=request.user, timezone=timezone_str)
            messages.success(request, "Timezone updated successfully!")
            return redirect('profile')
    else:
        form = TimezoneForm(initial={'timezone': timezone.get_current_timezone_name()})
    
    return render(request, 'update_timezone.html', {'form': form})

def update_language(request):
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            language_code = form.cleaned_data['language']
            # Change the language setting
            request.session[settings.LANGUAGE_COOKIE_NAME] = language_code
            messages.success(request, "Language updated successfully!")
            return redirect('profile')
    else:
        form = LanguageForm()

    return render(request, 'update_language.html', {'form': form})
