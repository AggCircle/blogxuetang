#login models.py

from django.db import models

class User(models.Model):
    '''用户表'''
 
    name = models.CharField(max_length=128)
    age = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    c_time = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name
 
    class Meta:
        ordering = ['c_time']
        verbose_name = '外部用户'
        verbose_name_plural = '外部用户'
        db_table = 'user'
