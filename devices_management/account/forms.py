import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Role


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    bse = forms.BooleanField(widget=forms.CheckboxInput())


    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("This username existed!")

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if self.cleaned_data['bse']==True:
            user = User.objects.get(username=self.cleaned_data['username'])
            Role.objects.filter(user_id=user.id).update(is_bse=True)

class ChangePwForm(forms.Form):
    current_password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    new_password_confirmation = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def update(self, uid):
        user = User.objects.get(id=uid)
        if user.password == self.cleaned_data['current_password'] and self.cleaned_data['new_password']==self.cleaned_data['new_password_confirmation']:
            user.set_password(self.cleaned_data['new_password'])
