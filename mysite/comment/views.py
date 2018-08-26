from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm
'''
def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    # 数据检查
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': '请先登录', 'redirect_to': referer})

    text = request.POST.get('text', '').strip() # 多个空格也是空内容
    if text == '':
        return render(request, 'error.html', {'message': '评论内容不能为空', 'redirect_to': referer})

    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})

    # 通过则保存数据
    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)  # 提交后重定向到原页面
'''


def update_comment(request):
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(
        request.POST, user=request.user)  # 实例化, 传递了用户信息，直接有表单类验证登录
    data = {}
    if comment_form.is_valid():
        # 通过则保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        # 判断回复
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        # data['comment_time'] = comment.comment_time.strftime(
        # '%Y-%m-%d %H:%M:%S')
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if parent is not None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''

    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)