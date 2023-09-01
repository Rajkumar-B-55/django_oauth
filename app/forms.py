from django import forms


class RegistrationForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
