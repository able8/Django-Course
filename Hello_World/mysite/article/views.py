from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Article

# Create your views here.
def article_detail(request, article_id):
    # article = Article.objects.get(id=article_id)
    article = get_object_or_404(Article, pk=article_id)
    context = {}
    context['article_obj'] = article
    # return render(request, 'article_detail.html', context)
    return render_to_response('article_detail.html', context)

def article_list(request):
    # articles = Article.objects.all()
    articles = Article.objects.filter(is_deleted=False)
    context = {}
    context['articles'] = articles
    return render_to_response('article_list.html', context)