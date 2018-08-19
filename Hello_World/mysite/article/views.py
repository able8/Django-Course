from django.shortcuts import render
from django.http import HttpResponse
from .models import Article

# Create your views here.
def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return HttpResponse('<h2>文章标题：%s </h2><hr> 文章内容：%s' % (article.title, article.content))