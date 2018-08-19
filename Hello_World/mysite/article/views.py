from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Article

# Create your views here.
def article_detail(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        context = {}
        context['article_obj'] = article
        return render(request, 'article_detail.html', context)
    except Article.DoesNotExist:
        raise Http404('not exit')