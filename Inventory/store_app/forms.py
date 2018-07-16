
from django.contrib.auth.forms import AuthenticationForm 
#from django import forms

from django import forms
from .models import Product


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('device_name', 'path_number', 'serial_number', 'device_type', 'location','status')
        