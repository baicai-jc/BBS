from django import forms  # forms组件所需模块
from app01 import models


class MyRegForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=8, min_length=3,
                               error_messages={
                                   'required': '用户名不能为空',
                                   'max_length': '用户名最多8位',
                                   'min_length': '用户名最少3位',
                               },
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
                               )

    password = forms.CharField(label="密码", max_length=8, min_length=3,
                               error_messages={
                                   'required': '密码不能为空',
                                   'max_length': '密码最多8位',
                                   'min_length': '密码最少3位',
                               },
                               widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                               )

    confirm_password = forms.CharField(label="确认密码", max_length=8, min_length=3,
                                       error_messages={
                                           'required': '确认密码不能为空',
                                           'max_length': '确认密码最多8位',
                                           'min_length': '确认密码最少3位',
                                       },
                                       widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                                       )

    email = forms.EmailField(label='邮箱',
                             error_messages={
                                 'required': '邮箱不能为空',
                                 'invalid': '邮箱格式不正确',
                             },
                             widget=forms.widgets.EmailInput(attrs={'class': 'form-control'})
                             )

    # 钩子函数
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 数据库中校验
        is_exists = models.UserInfo.objects.filter(username=username)
        if is_exists:
            # 提示信息
            self.add_error('username', '用户名已存在')

        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not password == confirm_password:
            self.add_error('confirm_password', '两次密码不一致')
        return self.cleaned_data
