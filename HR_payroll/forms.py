from django import forms
from .models import Salary


class MonthlySalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['amount']
