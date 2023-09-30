from django import forms
from administration.models import LoanApply


class ApplyForm(forms.ModelForm):
    class Meta:
        model = LoanApply
        fields = ['customer','amount']  # Specify the fields you want in the form

        widgets = {
        'amount': forms.NumberInput(attrs={'class': 'formbold-form-input','placeholder':''}),
       'customer': forms.Select(attrs={'class': 'formbold-form-input'}),  # Use Select widget for ForeignKey
        }

    