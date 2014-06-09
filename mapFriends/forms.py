from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value = False))

class RegisterForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(render_value=False))

    def clean_password_confirm(self):
    	password = self.cleaned_data['password']
    	password_confirm = self.cleaned_data['password_confirm']
    	if password == password_confirm:
    		pass
    	else:
    		raise forms.ValidationError('Passwords no coinciden')