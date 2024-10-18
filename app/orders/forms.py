from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['skill', 'description', 'amount']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
