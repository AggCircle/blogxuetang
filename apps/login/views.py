# login/views.py

from django.shortcuts import render,redirect
from apps.login.models import User
from .forms import UserForm, RegisterForm

def index(request):
    pass
    return render(request,'home.html')
 
def login(request):
	if request.session.get('is_login',None):
		return redirect('/home')

	if request.method == "POST":
		login_form = UserForm(request.POST)
		message = "请检查填写的内容！"
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			phone = login_form.cleaned_data['phone']
			try:
				user = User.objects.get(name=username)
				if user.phone == phone:
					request.session['is_login'] = True
					request.session['user_id'] = user.id
					request.session['user_name'] = user.name
					return redirect('/home/')
				else:
					message = "手机号与用户不匹配！"
			except:
				message = "用户不存在！"
		return render(request, 'login/login.html', locals())

	login_form = UserForm()
	return render(request, 'login/login.html', locals())
 
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/home/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            age = register_form.cleaned_data['age']
            phone = register_form.cleaned_data['phone']
            email = register_form.cleaned_data['email']
            same_name_user = User.objects.filter(phone=phone)
            same_username_user = User.objects.filter(name=username)
            if same_name_user and same_username_user:  # 用户名唯一
                message = '用户已经存在！'
                return render(request, 'login/register.html', locals())
            # 当一切都OK的情况下，创建新用户

            new_user = User.objects.create()
            new_user.name = username
            new_user.phone = phone
            new_user.age = age
            new_user.email = email
            new_user.save()
            return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())
 
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/home/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/home/")

