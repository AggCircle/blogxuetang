from django.conf.urls import url
from . import views

app_name = 'guestbook'

urlpatterns = [
    url(r'^message/',views.message_event,name='message'),
    url(r'^create/$', views.message_create, name='create'),
    url(r'^message_save/$', views.message_save, name='message_save'), 
]