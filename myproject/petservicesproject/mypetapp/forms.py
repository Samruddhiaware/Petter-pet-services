from django import forms
from .models import SPService

class createform(forms.ModelForm):
    class Meta:
        model = SPService
        fields = ['name', 'image', 'description', 'category', 'provider', 'location', 'price', 'duration', 'status', 'additional_info']

