#encoding: utf-8
from django.db import models
from apps.login.models import User
from apps.blog.models import Article

class Message(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='活动', on_delete=models.CASCADE)
    content=models.TextField(max_length=512)
    c_time=models.DateTimeField(auto_now_add=True)

	#为了显示
    def __str__(self):
        tpl = '<Message:[username={username}, content={content}, publish={c_time}]>'
        return tpl.format(username=self.username, content=self.content, publish=self.publish)
