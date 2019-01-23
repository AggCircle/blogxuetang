from django import forms
 
 
class UserForm(forms.Form):
    username = forms.CharField(label="姓名", max_length=128, widget=forms.TextInput(attrs={'id': 'username', 'placeholder': '姓名'}))
    phone = forms.CharField(label="手机号", max_length=256, widget=forms.TextInput(attrs={'id': 'phone', 'placeholder': '电话号'}))

class RegisterForm(forms.Form):
    username = forms.CharField(label="姓名", max_length=128, widget=forms.TextInput(attrs={'placeholder': '姓名', 'style':'background: #eae7e7 no-repeat; padding: 15px 10px 15px 15px;'}))
    age = forms.CharField(label="年龄",max_length=50 , widget=forms.TextInput(attrs={'placeholder': '年龄', 'style':'background: #eae7e7 no-repeat; padding: 15px 10px 15px 15px;'}))
    phone = forms.CharField(label="手机号",max_length=50 , widget=forms.TextInput(attrs={'placeholder': '电话号', 'style':'background: #eae7e7 no-repeat; padding: 15px 10px 15px 15px;'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'placeholder': '邮箱地址', 'style':'background: #eae7e7 no-repeat; padding: 15px 10px 15px 15px;'}))

