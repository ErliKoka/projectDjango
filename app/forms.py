from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = "Choose a unique username (letters, numbers, or @/./+/-/_ only)."
        self.fields['email'].help_text = "Enter a valid email address we can contact you at."
        self.fields['password1'].help_text = "Use 8+ characters. Mix letters, numbers, and symbols."
        self.fields['password2'].help_text = "Repeat your password to confirm."
       
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)