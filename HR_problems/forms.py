from .models import *
from django.forms import ModelForm, Textarea
from django import forms


class SoftwareForm(forms.Form):

    title = forms.CharField(max_length=100)
    issue = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Explain your issue!'
    )
    root_cause      =   forms.CharField(max_length=100)
    Symptoms        =   forms.CharField(max_length=100)
    hardware_item   =   forms.ModelChoiceField(queryset=Hardware.objects.all(), required=False)
    software_item   =   forms.ModelChoiceField(queryset=Software.objects.all(), required=False)

   
class SoftUpForm(forms.ModelForm):
    class Meta:
        model = Prob_software
        fields = ['current_status', 'solved', 'priority', 'impact',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': Textarea(attrs={'class': 'form-control'}),
        }
    
