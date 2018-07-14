from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Your email"
        }
    ))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        queryset = User.objects.filter(username=username)
        if queryset.exists():
            raise forms.ValidationError("Username is taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        queryset = User.objects.filter(email=email)
        if queryset.exists():
            raise forms.ValidationError("Email is already registered under another account.")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            raise forms.ValidationError("Passwords must match")
        return data


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
