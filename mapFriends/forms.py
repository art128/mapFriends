from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value = False))

class RegistroForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(render_value=False))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email in use')

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']

        if password == password_confirm:
            pass
        else:
            raise forms.ValidationError('Password dont match')
