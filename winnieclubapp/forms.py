from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Worker  # Make sure Worker is defined in models.py

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'role', 'photo']
