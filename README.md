# Django_Course
Python Django Web开发  入门到实践 视频地址：https://space.bilibili.com/252028233/#/

看视频整理要点笔记: 

## 01.什么是Django
#### 1. 什么是Django

- 官网：https://www.djangoproject.com
- 文档：https://docs.djangoproject.com/en/2.0/
- The web framework for perfectionists with deadlines.
- 在截止日期内，完美主义者使用的Web框架。
- Django was invented to meet fast-moving newsroom deadlines, while satisfying the tough requirements of experienced Web developers.
- Django的发明是为了满足紧急新闻编辑部的最后期限，同时满足经验丰富的Web开发人员的苛刻要求。
- Django makes it easier to build better Web apps  more quickly and with less code.
- Django让更快搭建好的Web应用变得更简单，并且代码更少。
  - 开发快到离谱，免费开源，处理了许多Web开发繁琐的事，令使用者专注业务
  - 令人放心的安全
  - 可拓展性强

#### 2. Django版本选择

- https://www.djangoproject.com/download/
- 本项目基于 Python3.6+ 和 Django2.0
![版本图](https://www.djangoproject.com/s/img/release-roadmap.e844db08610e.png)

## 02.入门 Hello World
- 入门仪式：创建项目，输出Hello, world
- 创建项目命令：`django-admin  startproject mysite`
- Django项目基本结构

```
mysite
    ├ mysite            Pyhton 包
    │   └ - _init__.py  
    │   └ - settings.py 全局设置文件
    │   └ - urls.py     全局路由控制
    │   └ - wsgi.py     服务器使用的wsgi部署文件
    └  manage.py        项目管理
```

- 响应请求
    - 客户端 打开网址发送请求-》Urls 处理请求 -》Views 响应请求，返回内容
- 启动本地服务 `python manage.py runserver`
- 执行数据库迁移，新建数据库 `python manage.py migrate`
- 创建超级管理员用户`python manage.py createsuperuser`
- 管理员页面 http://127.0.0.1:8000/admin/
    
## 03.Django基本应用结构
- 创建Django App `python manage.py startapp article`
- 如果页面比较多，将相似的内容用模版来管理，数据抽象为模型Models
- 创建数据的模型models

```python
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
```
- 创建模型后，先需要生成数库迁移文件，再执行数据库迁移
    - 首先要在`settings.py`中，`INSTALLED_APPS` 添加app name
    - `python manage.py makemigrations`
    - `python manage.py migrate`
       
``` py
# 生成的数据库迁移文件
class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
            ],
        ),
    ]

```

- 将模型注册到后台管理页面

```py
# admin.py
from .models import Article
# Register your models here.
admin.site.register(Article)
```
- 进入后台找到Article 管理，添加修改数据
- 设置语言和时区`settings.py`

```py
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
```

## 04.使用模版显示内容
- 查看文章页面
    - 如何通过一个处理方法获取文章唯一的标识
- ` path('article/<int:article_id>', article_detail, name='article_detail'),`
    - `<int:article_id>` 默认是字符串，添加int指定整型
- 模型的`objects`是获取和操作模型的对象


```py
from .models import Article
Article.objects.get(条件) # 根据条件获取数据
Article.objects.all()    # 获取所有数据
Article.objects.filter(条件) # 根据条件过滤数据

article = Article.objects.get(id=article_id)
    return HttpResponse('<h2>文章标题：%s </h2><hr> 文章内容：%s' % (article.title, article.content))
```

- 获取不存在的文章，返回404页面

```py
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise Http404('not exit')
```

- 使用模版，前端页面和后端代码分离，降低耦合性

- 查看 django 源码，了解函数功能
    - VS code 右键 速览定义 可以显示源码
    - 找到安装路径`pip show django`
    - 进入查看源码文件

- 简化，用render_to_response省略请求参数，用get_object_or_404代替异常处理

```py
# article = Article.objects.get(id=article_id)
article = get_object_or_404(Article, pk=article_id)
context = {}
context['article_obj'] = article
# return render(request, 'article_detail.html', context)
return render_to_response('article_detail.html', context) # 不需要request参数l
```
- 获取文章列表
    - 用url模版代替硬编码，方便后续修改
    - `<a href="/article/{{ article.pk }}">`
    - `<a href="{% url 'article_detail' article.pk %}">`


```py
def article_list(request):
    articles = Article.objects.all()
    context = {}
    context['articles'] = articles
    return render_to_response('article_list.html', context)
```
- 路由管理，总urls包含app的urls，总分结构，便于维护

```py
# 总路由
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('article/', include('article.urls'))
]
# app 路由
urlpatterns = [
    # localhost:8000/article/
    path('', views.article_list, name='article_list'),
    path('<int:article_id>', views.article_detail, name='article_detail'),
]

```

## 05.定制后台和修改模型
- 定制后台
    - 设置模型显示 `__str__`
    - 定制模型admin后台管理页面
    
```py
# 设置模型显示 models.py
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    def __str__(self):
       return '<Article: %s>' % self.title 

       
# admin.py
# Register your models here.
@admin.register(Article) # 使用装饰器更方便醒目
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')
    # ordering = ('-id', )  倒序
    ordering = ('id', )

#admin.site.register(Article, ArticleAdmin)
```

- 修改模型models，修改后台显示字段
    - 每次修改模型需要更新数据库
    - `python manage.py makemigrations`
    - `python manage.py migrate`
    - 需要设置默认值

```py
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    # created_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1) 
    is_deleted = models.BooleanField(default=False)
    readed_num = models.IntegerField(default=0)

# admin.py 后台显示字段
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author','is_deleted', 'created_time', 'last_updated_time', 'content')
    # ordering = ('-id', )  倒序
    ordering = ('id', )   
    
# 使用，过滤删除的  views.py
def article_list(request):
    # articles = Article.objects.all()
    articles = Article.objects.filter(is_deleted=False)
```
- 数据库的几个概念：主键，外键，索引，唯一索引
    - 主键`primary key`，是能确定一条记录的唯一标识，如id
    - 外键`foreign key`，外键用于与另一张表的关联，用于保持数据的一致性，表的外键是另一表的主键。
    - 索引`index`，为了提高查询排序的速度。
    - 聚集索引，**在索引页里直接存放数据**，而**非聚集索引**在索引页里存放的是**索引，这些索引指向专门的数据页的数据。**
    - 主键和外键是把多个表组织为一个有效的关系数据库的粘合剂。主键和外键的设计对物理数据库的性能和可用性都有着决定性的影响。

## 06.开始完整制作网站
- 想清楚为什么做网站，动力影响学习热情，原因决定最终结果
    - 兴趣爱好
    - 学习一门技术
    - 工作需要，业务需求
    - 创业项目需要
- 如何用Django开发网站
    - 要做什么，设计网站原型
        - 业务流程
        - 功能模块
        - 前端布局
        - 后端模型
- 接下来的教程
    - 目的
        1. 通过完整的开发过程学习Django
        2. 对一般的网站开发有全面的认识
    - 途径
        - 制作个人博客网站
- 个人博客网站
    - 项目管理
        - IDE
        - 本地虚拟开发环境
        - 版本控制Git／Github
    - 前端开发
        - html+javascript+CSS
        - jQuery
        - Bootstrap
        - ajax
    - 后端开发
        - 博客管理和展示
        - 用户登录和注册
        - 评论和回复
        - 点赞
    - 数据库和服务器
        - MySQL
        - Linux
        - 网站部署
        
## 07.构建个人博客网站
- 网站的功能模块 即 Django App
    - 博客
        - 博文
        - 博客分类
        - 博客标签
    - 评论
    - 点赞
    - 阅读
    - 用户

- 开启本地虚拟环境
    - 隔开python项目的运行环境
    - 避免多个项目之前python库的冲突
    - 完整便捷导出python库的列表
 
```sh
pip install virtualenv
virtualevn mysit_env # 创建 虚拟环境
activate
deactivate
pip freeze   > requirements.txt # 一键导出
pip install -r requirements.txt # 一键安装
```
   
- 初步创建blog应用
    - 博文 + 博客分类
    - 为了好管理，约定一篇博客只属于一个分类
  
```sh
django-admin startproject mysite
cd mysite
python manage.py startapp blog
python manage.py migrate
python manage.py createsuperuser
# 修改模型，先在INSTALLED_APPS中添加app name
python manage.py makemigrations
python manage.py migrate
``` 
- 创建Blog模型和注册admin后台模型管理页面

```py
# models.py
# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Blog: %s>' % self.title
        
# admin.py
from django.contrib import admin
from .models import BlogType, Blog
# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'created_time', 'last_updated_time')
    ordering = ('id',)   
```

## 08.常用的模版标签和过滤器

- 继续搭建blog
    - models 
    - admin
    - views
    - urls
    - templates

- 常用的模版标签
    - 循环 for 
    - 条件 if, ifequal, ifnoequal
    - 链接 url
    - 模版嵌套 block、extends、include
    - 注释 {# #}
- 常用的过滤器
    - 日期 data
    - 字数截取 truncatechars truncatechars_html
    - 长度 length
- 参考：[Django Built-in template tags and filters](https://docs.djangoproject.com/en/2.0/ref/templates/builtins/#built-in-filter-reference)

```
<p>一共有 {{ blogs|length }} 篇博客 </p>

context['blogs_count'] = Blog.objects.all().count
{{ blogs_count }}
```

## 09.模版嵌套

- `{% extends "base.html" %}` 引用基础模版
- `<title>{% block title %}{% endblock title %}</title>` 块
- `{% block content %}{% endblock content %}`

