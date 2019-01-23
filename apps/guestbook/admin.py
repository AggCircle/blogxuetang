from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
	list_display = ("user", "article", "content", "c_time")
	list_filter = ("article", "c_time")
	search_fields = ("article", "user")
	ordering = ['c_time','article']
 
admin.site.register(Message, MessageAdmin)