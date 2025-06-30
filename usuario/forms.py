from django import forms


class LoginForm(forms.Form) :
    username = forms.CharField(label='Nome', max_length=100)
    senha    = forms.CharField(label='senha', max_length=100)






