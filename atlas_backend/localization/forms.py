# forms.py
from django import forms
import pytz

class TimezoneForm(forms.Form):
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in pytz.all_timezones]
    )

class LanguageForm(forms.Form):
    language = forms.ChoiceField(
        choices=[('en', 'English'), ('fr', 'French'), ('es', 'Spanish'), ('de', 'German')]
    )
