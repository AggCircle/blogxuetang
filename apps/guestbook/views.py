from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import models
from apps.blog.models import Article
from apps.login.models import User

# Create your views here.
def message_event(article):
	messages = models.Message.objects.filter(article=article).order_by("c_time").reverse()
	return messages

@csrf_exempt
def message_create(request):
    return render(request, 'guestbook/create.html')

@require_POST
@csrf_exempt
def message_save(request):
	if request.session.get('is_login',None):
		user_id = request.session.get('user_id',None)
		user = User.objects.get(id=user_id)
		content = request.POST.get("content")
		article = Article.objects.get(id=request.POST.get('id'))
		message = models.Message(content=content, user=user, article=article)
		message.save()
		return HttpResponse('{"status":"success"}', content_type='application/json')
	else:
		return HttpResponse('{"status":"fail"}', content_type='application/json')
