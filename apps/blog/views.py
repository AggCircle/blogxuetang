from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.blog.models import Article, Category, Tag, CustomerApply
from apps.login.models import User
from apps.guestbook.models import Message
from apps.guestbook.views import message_event, message_save
import time
import datetime

categories = Category.objects.all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象
months = Article.objects.datetimes('pub_time', 'month', order='DESC')


def home(request):  # 主页
    posts = Article.objects.filter(status='p', pub_time__isnull=False).order_by('pub_time')  # 获取全部(状态为已发布，发布时间不为空)Article对象
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list, 'category_list': categories, 'months': months})

def result(request):  # 查询
    if request.session.get('is_login',None):
        try:
            user_id = request.session.get('user_id',None)
            infos = CustomerApply.objects.filter(user_id=user_id)
            details = []
            for info in infos:
                item = {}
                item['name'] = info.name
                item['article'] = info.article.title
                if info.verify == 'responsed':
                    item['state'] = '报名成功'
                elif info.send:
                    item['state'] = '已发送邀请'
                    item['id'] = info.id
                else:
                    item['state'] = '待管理员确认'
                details.append(item)
            return render(request, 'detail.html',{'details': details})
        except:
            return render(request, 'detail.html')
    else:
        return redirect('/login/')


def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
        tags = post.tags.all()
        messages = message_event(article=str(id))
        count = messages.count()
        next_post = post.next_article()  # 上一篇文章对象
        prev_post = post.prev_article()  # 下一篇文章对象
    except Article.DoesNotExist:
        raise Http404
    return render(
        request, 'post.html',
        {
            'post': post,
            'tags': tags,
            'count': count,
            'category_list': categories,
            'next_post': next_post,
            'prev_post': prev_post,
            'months': months,
            'messages' : messages
        }
    )


def search_category(request, id):
    posts = Article.objects.filter(category_id=str(id))
    category = categories.get(id=str(id))
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'category.html',
                  {'post_list': post_list,
                   'category_list': categories,
                   'category': category,
                   'months': months
                  }
    )


def search_tag(request, tag):
    posts = Article.objects.filter(tags__name__contains=tag)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'tag.html', {
        'post_list': post_list,
        'category_list': categories,
        'tag': tag,
        'months': months
        }
    )


def archives(request, year, month):
    posts = Article.objects.filter(pub_time__year=year, pub_time__month=month).order_by('-pub_time')
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'archive.html', {
        'post_list': post_list,
        'category_list': categories,
        'months': months,
        'year_month': year+'年'+month+'月'
        }
    )

@require_POST
@csrf_exempt
def blog_save(request):
    if request.session.get('is_login',None):
        user_id = request.session.get('user_id',None)
        user_info = User.objects.filter(id=user_id)

        blogs = CustomerApply.objects.all()
        name = user_info[0].name
        age = user_info[0].age
        email = user_info[0].email
        phone = user_info[0].phone
        id_activity = request.POST.get('id')
        article = Article.objects.get(id=id_activity)
        user = User.objects.get(id=user_id)
        for blog in blogs:
            if blog.phone == phone and blog.article == article:
                return HttpResponse('{"status":"fail"}', content_type='application/json')
        student = CustomerApply(name=name, age=age, email=email, phone=phone, user_id=user, article=article)
        student.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponse('{"status":"login"}', content_type='application/json')

# 报名筛选
@csrf_exempt
def blog_choice(request):
    if request.POST:
        check_box_list = request.POST.getlist("check_box_list")
        for lable in check_box_list:
            student = CustomerApply.objects.get(id=lable)
            send_html_mail(adress=student.email, ID=lable, mss=student.article.activity_words)
            CustomerApply.objects.filter(id=lable).update(send=True,comment='已发送')
            time.sleep(1)
        return render(request, "customer_filter.html", {"blogs":CustomerApply.objects.all().order_by("article")})
    blogs = CustomerApply.objects.all().order_by("article")
    return render(request, "customer_filter.html",{"blogs":blogs})

# 发送邮件
def blog_send(adress, ID, mss):
# send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    subject = '华夏科技学堂'
    message = '%s确认参加请点击'%mss+'http://www.hxkjxt.top/affirm?ID='+ID+'''
您可登录 http://www.hxkjxt.top/result/ 查询报名信息,成功确认后若未能准时参加活动将影响您的信誉度。'''
    send_mail(
        subject,
        message,
        'hxkjxt@sina.com',
        [adress],
        fail_silently=False,
    )

def send_html_mail(adress, ID, mss, time):
    urls = 'http://www.hxkjxt.top/affirm?ID='+ID
    subject = '请确认是否参加中国科技馆华夏科技学堂活动'
    html_content = loader.render_to_string(
                     'mail.html',               #需要渲染的html模板
                     {
                        'message': mss,
                        'activity_time': time,
                        'urls': urls,    #参数
                     }
               )
    msg = EmailMessage(subject, html_content, 'hxkjxt2018@163.com', [adress,])
    msg.content_subtype = "html" # Main content is now text/html
    msg.send()

# 确认报名
@csrf_exempt
def affirm(request):
    if request.POST:
        ID = request.POST.get('affirm_id')
    else:
        ID = request.GET['ID']
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    student=CustomerApply.objects.get(id=ID)
    deadline = student.article.deadline.strftime("%Y%m%d%H%M%S")
    if now > deadline:
        return render(request, 'timeout.html')
    else:
        stutent=CustomerApply.objects.filter(id=ID).update(verify='responsed', comment='已确认')
        site = student.article.activity_site
        time_active = student.article.pub_time
        return render(request, 'affirm.html', {"site":site, "time_active":time_active})
