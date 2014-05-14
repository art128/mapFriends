from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value = False))

class RegistroForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput())
    uid = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.TextInput())
    access_token = forms.CharField(widget=forms.TextInput())
    expire_token = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(render_value=False))
