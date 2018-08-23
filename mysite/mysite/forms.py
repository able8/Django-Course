from django import forms
from django.contrib import auth


# 定制登录表单
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', required=True) # 默认为True
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
