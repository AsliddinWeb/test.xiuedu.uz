from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg fs-15px'
    }))
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg fs-15px'
    }))


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize field labels
        self.fields['old_password'].label = 'Hozirgi parol'
        self.fields['new_password1'].label = 'Yangi parol'
        self.fields['new_password2'].label = 'Yangi parolni tasdiqlang'

        # Add custom widgets
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Hozirgi parolni kiriting'})
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Yangi parolni kiriting'})
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Yangi parolni tasdiqlashni kiriting'})