from django import forms
from rbac.models import Permission, Menu, Role, UserInfo
from django.contrib.auth.models import User
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ("title",)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('uname',)