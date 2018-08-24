from django import forms
from django.contrib import auth


# 定制登录表单
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                        required=True, # 默认为True
                        widget=forms.TextInput(attrs={'class': 'form-control',
                            'placeholder':'请输入用户名'}))
                        # 设置渲染后的html的属性
                        
    password = forms.CharField(label='密码',
                        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'请输入密码'}))

    # 验证数据方法
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data