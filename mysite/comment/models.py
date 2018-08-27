import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


# 多线程发送邮件
class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
        )


class Comment(models.Model):
    # 下面3行用来关联任意类型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)

    # parent_id = models.IntegerField(default=0) # 用于回复功能,或使用如下自己的外键
    root = models.ForeignKey(
        'self',
        related_name='root_comment',
        null=True,
        on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        related_name='parent_comment',
        null=True,
        on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        User, related_name='replies', null=True, on_delete=models.CASCADE)

    def send_comment_mail(self):
        # 发送邮件通知
        if self.parent is None:
            # 评论我的博客
            # 发送邮箱
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复你的博客'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_mail.html', context)
            send_comment_thread = SendMail(subject, text, email)
            send_comment_thread.start()

    def __str__(self):
        return self.text  # 显示评论内容

    class Meta:
        # ordering = ['-comment_time'] # 时间逆序，最新的在最前面
        ordering = ['comment_time']  # 时间逆序，最新的在最前面
