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



from django import forms
from .models import Sale, StockItem

from django import forms
from .models import Sale, StockItem

from django import forms
from .models import StockItem

from django import forms
from .models import Sale, StockItem

class SaleForm(forms.ModelForm):
    stock_item = forms.ModelChoiceField(queryset=StockItem.objects.all())

    class Meta:
        model = Sale
        fields = '__all__'
