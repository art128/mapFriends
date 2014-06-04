from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value = False))

class RegistroForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(render_value=False))