from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
    email = forms.CharField(widget=forms.EmailInput(attrs={'required':'required','class':'input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'required':'required','class':'input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'required':'required','class':'input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'required':'required','class':'input'}))
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required':'required','class':'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required':'required','class':'input'}))