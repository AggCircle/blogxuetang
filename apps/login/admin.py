from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
	list_display = ("name", "age", "phone", "email")
	list_filter = ("name", "phone")
	search_fields = ("name", "phone")
	ordering = ['phone','name']
 
admin.site.register(User, UserAdmin)