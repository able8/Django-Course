from django.shortcuts import render
from django.http import HttpResponse
from .models import Article

# Create your views here.
def article_detail(request, article_id):
    
    return HttpResponse('文章 id：%s' % article_id)