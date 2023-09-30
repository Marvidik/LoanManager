from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customers

class CustomRegistrationForm(UserCreationForm):
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password','type':'password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm Password'}),
        }

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'branch': forms.Select(attrs={'class': 'formbold-form-input'}),  # Use Select widget for ForeignKey
            'gender': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'occupation': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'state': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'passport': forms.FileInput(attrs={'class': 'form-control','placeholder':''}),
            'business_name': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'bussiness_address': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'age': forms.NumberInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'phone_number': forms.NumberInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'home_address': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'card_number': forms.NumberInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            

            'guarantors_name': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'guarantors_phone': forms.NumberInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'guarantors_address': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'goccupation': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
            'gstate': forms.TextInput(attrs={'class': 'formbold-form-input','placeholder':''}),
        }

from django import forms
from .models import Paid  # Import the Paid model from your app's models

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Paid
        fields = ['loan','amount']  # Specify the fields you want in the form

        widgets = {
        'amount': forms.NumberInput(attrs={'class': 'formbold-form-input','placeholder':''}),
        'loan': forms.Select(attrs={'class': 'formbold-form-input'}),  # Use Select widget for ForeignKey
        }

    
