from django.db import models
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum

# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    # content = models.TextField()
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # readed_num = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    '''
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
    '''
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(Blog)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
        

    def __str__(self):
        return '<Blog: %s>' % self.title

    class Meta:
        # ordering = ['-created_time']
        ordering = ['created_time']

'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
    # 或者 blog = models.ForeignKey(Blog, on_delete=models.DO_NOTHING)
'''