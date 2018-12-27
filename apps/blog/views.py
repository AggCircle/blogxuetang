from django.shortcuts import render
from apps.blog.models import Article, Category, Tag, CustomerApply
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import time
import datetime

categories = Category.objects.all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象
months = Article.objects.datetimes('pub_time', 'month', order='DESC')


# Create your views here.
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
    if request.method == 'POST':
        phone = request.POST.get('phone')
        infos = CustomerApply.objects.filter(phone=phone)
        apply = []
        for info in infos:
            item = {}
            item['name'] = info.name
            item['age'] = info.age
            item['phone'] = info.phone
            item['email'] = info.email
            item['article'] = info.article.title
            if info.verify == 'responsed':
                item['state'] = '报名成功'
            elif info.send:
                item['state'] = '已发送邀请'
            else:
                item['state'] = '待管理员确认'
            apply.append(item)
        response = JsonResponse({"details": apply})
        return response

    return render(request, 'detail.html')


def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
        tags = post.tags.all()
        next_post = post.next_article()  # 上一篇文章对象
        prev_post = post.prev_article()  # 下一篇文章对象
    except Article.DoesNotExist:
        raise Http404
    return render(
        request, 'post.html',
        {
            'post': post,
            'tags': tags,
            'category_list': categories,
            'next_post': next_post,
            'prev_post': prev_post,
            'months': months
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
    blogs = CustomerApply.objects.all()
    name = request.POST.get('user')
    age = request.POST.get('age')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    id_activity = request.POST.get('id')
    article = Article.objects.filter(id=id_activity)[0]
    for blog in blogs:
        if blog.phone == phone and blog.article == article:
            return HttpResponse('{"status":"fail"}', content_type='application/json')
    student = CustomerApply(name=name, age=age, email=email, phone=phone, article=article)
    student.save()
    return HttpResponse('{"status":"success"}', content_type='application/json')

# 报名筛选
@csrf_exempt
def blog_choice(request):
    if request.POST:
        check_box_list = request.POST.getlist("check_box_list")
        for lable in check_box_list:
            student = CustomerApply.objects.get(id=lable)
            blog_send(adress=student.email, ID=lable, mss=student.article.activity_words)
            CustomerApply.objects.filter(id=lable).update(send=True,comment='已发送')
            time.sleep(0.3)
        return render(request, "customer_filter.html", {"blogs":CustomerApply.objects.all().order_by("article")})
    blogs = CustomerApply.objects.all().order_by("article")
    return render(request, "customer_filter.html",{"blogs":blogs})

# 发送邮件
def blog_send(adress, ID, mss):
# send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    subject = '华夏科技学堂'
    message = '%s确认参加请点击'%mss+'http://www.hxkjxt.top/affirm?ID='+ID+'''
您可登录 http://www.hxkjxt.top/result/ 查询报名信息,成功确认后若未能准时参加活动将影响您的信誉度。'''
    print(message)
    send_mail(
        subject,
        message,
        'hxkjxt@sina.com',
        [adress],
        fail_silently=False,
    )

# 确认报名
def affirm(request):
    now = datetime.datetime.now().strftime("%d%H%M%S")
    ID = request.GET['ID']
    student=CustomerApply.objects.get(id=ID)
    deadline = student.article.deadline.strftime("%d%H%M%S")
    if now > deadline:
        return HttpResponse("对不起，已过规定的最后确认时间，请留心下次活动！")
    else:
        stutent=CustomerApply.objects.filter(id=ID).update(verify='responsed', comment='已确认')
        site = student.article.activity_site
        time_active = student.article.pub_time
        return render(request, 'affirm.html', {"site":site, "time_active":time_active})
