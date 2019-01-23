"""jbt_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from apps.blog.views import home, detail, search_category, search_tag, archives, blog_save, result, blog_send, blog_choice, affirm, send_html_mail
from apps.login.views import login, register, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('articles/<int:id>/', detail, name='detail'),
    path('category/<int:id>/', search_category, name='category_menu'),
    path('tag/<str:tag>/', search_tag, name='search_tag'),
    path('archives/<str:year>/<str:month>', archives, name='archives'),
    path('summernote/', include('django_summernote.urls')),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^save', blog_save, name="blog_save"),
    url(r'^result', result, name='result'),
    url(r'^send', blog_send, name="blog_send"),
    url(r'^filter', blog_choice, name="blog_choice"),
    url(r'^affirm', affirm, name="affirm"),
    path('sent/', send_html_mail, name='send_html'),
    url(r'^login/', login),
    url(r'^register/', register),
    url(r'^logout/', logout),
    url(r'^guestbook/', include('apps.guestbook.urls',namespace='guestbook')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})
    ]