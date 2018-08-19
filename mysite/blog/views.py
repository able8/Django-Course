from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog

def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    return render_to_response('blog_list.html', context)

def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render_to_response('blog_detail.html', context)
