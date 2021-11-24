from django.forms import ModelForm
from django import forms
from Athena.models import Stock
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256)
    captcha = CaptchaField()  # 验证码字段

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username:
            msg = '用户名不能为空'
            self.add_error('username', msg)
        if not password:
            msg = '密码不能为空'
            self.add_error('password', msg)

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label="确认密码", max_length=256,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not username:
            msg = '用户名不能为空'
            self.add_error('username', msg)
        if not password:
            msg = '密码不能为空'
            self.add_error('password', msg)
        if not confirm_password:
            msg = '密码确认不能为空'
            self.add_error('confirm_password', msg)
        if password != confirm_password:
            msg = '两次输入的密码不同'
            self.add_error('password', msg)
        user = User.objects.filter(username=username)
        if user:
            msg = '用户名已存在'
            self.add_error('username', msg)
    # captcha = CaptchaField(label='验证码')
