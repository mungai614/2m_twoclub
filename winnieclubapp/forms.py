from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Worker  # Make sure Worker is defined in models.py
from datetime import date

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

from django import forms
from .models import Sale, StockItem

from django import forms
from .models import Sale, StockItem
from django.core.exceptions import ValidationError

class SaleForm(forms.ModelForm):
    stock_item = forms.ModelChoiceField(queryset=StockItem.objects.all(), label="Product")
    quantity_sold = forms.IntegerField(min_value=1, label="Quantity to sell")
    date_sold = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=date.today)

    class Meta:
        model = Sale
        fields = ['stock_item', 'quantity_sold', 'date_sold']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially no buying/selling price inputs since they're auto-filled on backend

    def clean_quantity_sold(self):
        qty = self.cleaned_data.get('quantity_sold')
        stock_item = self.cleaned_data.get('stock_item')
        if stock_item and qty:
            if qty > stock_item.quantity:
                raise ValidationError(f"Not enough stock. Available quantity: {stock_item.quantity}")
        return qty

