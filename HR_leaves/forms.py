from django import forms
from .models import LeaveApplication
from HR_user_profiles.models import Profile
from django.contrib.auth.models import User

class CreateLeaveForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = '__all__'
        exclude = ['approved','employee','created_on']

class AssignForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['assign']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']