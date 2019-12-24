from django import forms
from django.contrib.auth.models import User
from rbac.models import UserInfo

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",)
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("密码不一致")
        return cd['password2']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("uname", "email", "phone", "roles")

