from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "Username"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': "Email address"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': "Password"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': "Confirm password"
        })
    )
    class Meta:
        model = UserAccount
        fields = ['username', 'email']

    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'