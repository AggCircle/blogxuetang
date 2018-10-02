from django.contrib import admin
from .models import Article, Category, Tag, CustomerApply
from django_summernote.admin import SummernoteModelAdmin
from .views import blog_send
# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)

def send_mail(modeladmin, request, queryset):
	for obj in queryset:
		blog_send(adress=obj.email, ID=str(obj.id))
	queryset.update(send=True,comment='已发送')
send_mail.short_description = "发送邮件"

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)  # 给content字段添加富文本

class CustomerApplyAdmin(admin.ModelAdmin):
	list_display = ("name", "age", "phone", "email", "article", "comment")
	list_filter = ("article", "comment")
	search_fields = ("name", "phone", "article")
	ordering = ['article','name']
	actions = [send_mail]
admin.site.register(CustomerApply, CustomerApplyAdmin)
admin.site.register(Article, PostAdmin)