from django import forms
from .models import Product


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        label = {'name': 'Product name',
                 'category': 'Product category', 'price': 'Product Price'}
