from .models import Expenses
from django import forms


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'
        exclude = ['employee', 'approved']