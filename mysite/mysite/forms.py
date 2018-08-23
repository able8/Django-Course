from django import forms
from django.contrib import auth


# 定制登录表单
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', required=True) # 默认为True
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

    # 验证数据方法
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        elif:
            self.cleaned_data['user'] = user
        return self.cleaned_data