# Django_Course

Python Django Web开发  入门到实践 视频地址：<https://space.bilibili.com/252028233/>

看视频整理要点笔记:

## 01.什么是Django

### 1. 什么是Django

- 官网：<https://www.djangoproject.com>
- 文档：<https://docs.djangoproject.com/en/2.0/>
- The web framework for perfectionists with deadlines.
- 在截止日期内，完美主义者使用的Web框架。
- Django was invented to meet fast-moving newsroom deadlines, while satisfying the tough requirements of experienced Web developers.
- Django的发明是为了满足紧急新闻编辑部的最后期限，同时满足经验丰富的Web开发人员的苛刻要求。
- Django makes it easier to build better Web apps  more quickly and with less code.
- Django让更快搭建好的Web应用变得更简单，并且代码更少。
    - 开发快到离谱，免费开源，处理了许多Web开发繁琐的事，令使用者专注业务
    - 令人放心的安全
    - 可拓展性强

### 2. Django版本选择

- <https://www.djangoproject.com/download/>
- 本项目基于 Python3.6+ 和 Django2.0 ![版本图](https://www.djangoproject.com/s/img/release-roadmap.e844db08610e.png)

## 02.入门 Hello World

- 入门仪式：创建项目，输出Hello, world
- 创建项目命令：`django-admin  startproject mysite`
- Django项目基本结构

```sh
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
- 管理员页面 <http://127.0.0.1:8000/admin/>
    
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

```py
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
- `path('article/<int:article_id>', article_detail, name='article_detail'),`
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

```js
<p>一共有 {{ blogs|length }} 篇博客 </p>

context['blogs_count'] = Blog.objects.all().count
{{ blogs_count }}
```

## 09.模版嵌套

- `{% extends "base.html" %}` 引用基础模版
- `<title>{% block title %}{% endblock title %}</title>` 块
- `{% block content %}{% endblock content %}`

- 全局模版文件夹, 存放公共模版文件
    - 在`manage.py`目录创建文件夹`templates`，存放公共模版文件
    - 设置能够找到目录`settings - TEMPLATES - DIRS`
    - `os.path.join(BASE_DIR, 'templates'),`
    - 将 `base.html` 放到公共模版文件夹
- 模版文件设置建议，为了方便迁移和公有，放到project的templates文件夹
    - 为了防止名字冲突，在templates新建app name的文件夹，防止混淆
    - 修改views.py里的文件路径

## 10.使用CSS美化页面

- 页面设计
    - 导航栏：xxx的网站  首页 
    - 主体内容
    - 尾注

- 使用CSS 层叠样式表，修饰html
    - 使用Chrome浏览器审查元素，方便调试修改css，改好了再复制样式

- 新建static文件夹，专门存放静态文件，css js 图片
    - 在`manage.py`目录创建文件夹`static`，存放静态文件
    - 设置能够找到目录`settings - STATICFILES_DIRS`
    - `os.path.join(BASE_DIR, 'static')`
    - 引用`<link rel="stylesheet" href="/static/base.css">`
    - 或者 先`{% load staticfiles %}`
    - 再`<link rel="stylesheet" href="{% static 'base.css' %}">`

## 11.CSS框架协助前端布局

- 为什么使用CSS框架
    - 让web开发更迅速、简单
    - 使用现成的框架 省时又省力
- 如何选择CSS框架
    - 易用性
    - 兼容性
    - 大小、效果和功能
- Bootstrap 
    - 文档齐全，使用简单
    - 兼容较多浏览器，非轻量级
    - 响应式布局、移动设备优先
    - 组件齐全，扁平简洁
- 部署Bootstrap
    - 打开官网 <http://www.Bootcss.com>
    - 下载 [链接](https://v3.bootcss.com/getting-started/#download) 、引用、使用
    - `mini`是压缩过的体积小
    - 组件 [字体图标](https://v3.bootcss.com/components/)
    - [布局容器](https://v3.bootcss.com/css/#overview-container)
    - [栅格系统](https://v3.bootcss.com/css/#grid)
    - html 自动补全技巧 div.nav  li*2>2  按回车

## 12.Bootstrap响应式布局

- 添加博客列表和分类两栏，并根据屏幕自适应调整位置大小
- [栅格系统原理和代码](https://v3.bootcss.com/css/#grid)
- [博客分类使用的面板代码](https://v3.bootcss.com/components/#panels)
- 添加 [框架自带的图标](https://v3.bootcss.com/components/#glyphicons)
- Django静态文件命名空间
    - 为了避免冲突问题 `static/appname/xxx.css`

## 13.分页和shell命令行模式

- 通过讲解分页功能进一步夯实基础，包括shell命令行模式、模型操作、模版标签、分页器、GET请求。
- 为什么需要分页? 
    - 当博客文章数过多，全部加载过慢，就需要分页加载
- shell 命令行模式快速学习实践，添加博客
    - `python manage.py shell`
    - for 执行新增博客代码

- 模型新增对象

```python
python manage.py shell
from blog.models import Blog
blog = Blog() # 实例化
blog.title = 'xxx'
...
blog.save()
```

- shell 命令行 模式 操作模型

```python
>>> from blog.models import Blog
>>> dir()
['Blog', '__builtins__']
>>> Blog.objects.all()
<QuerySet [<Blog: <Blog: 第一篇博客>>, <Blog: <Blog: 第二篇博客>>, <Blog: <Blog: 第三篇博客>>, <Blog: <Blog: 第四篇长内容>>]>
>>> Blog.objects.count()
4
>>> blog = Blog()
>>> dir()
['Blog', '__builtins__', 'blog']
>>> blog.title = 'shell 下第1篇'
>>> blog.content = 'xxxx'
>>> from blog.models import BlogType
>>> BlogType.objects.all()
<QuerySet [<BlogType: 随笔>, <BlogType: 感悟>, <BlogType: 其他>]>
>>> BlogType.objects.all()[2]
<BlogType: 其他>
>>> blog_type = BlogType.objects.all()[2]
>>> blog.blog_type = blog_type
>>> from django.contrib.auth.models import User
>>> User.objects.all()
<QuerySet [<User: able>]>
>>> user = User.objects.all()[0]
>>> blog.author = user
>>> blog.save()
>>> Blog.objects.all()
<QuerySet [<Blog: <Blog: 第一篇博客>>, <Blog: <Blog: 第二篇博客>>, <Blog: <Blog: 第三篇博客>>, <Blog: <Blog: 第四篇长内容>>, <Blog: <Blog: shell 下第1篇>>]>
>>> dir(blog) # 查看所有 属性和方法，方便稍后调用

# 批量添加
>>> for i in range(1, 31):
...     blog = Blog()
...     blog.title = 'for %s' % i
...     blog.content = 'xxxx:%s' % i
...     blog.blog_type = blog_type
...     blog.author = user
...     blog.save()
...
>>> Blog.objects.all().count()
35
```

- 分页器实现分页
    - 导入`from django.core.paginator import Paginator`
    - 实例化`paginator = Paginator(object_list, each_page_count)`
    - 具体页面`page1 = paginator.page(1)`

```python
>>> from django.core.paginator import Paginator
>>> from blog.models import Blog
>>> blogs = Blog.objects.all()
>>> blogs.count()
35
>>> paginator = Paginator(blogs, 10)
<string>:1: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'blog.models.Blog'> QuerySet.
# 需要给模型添加 排序方式
    class Meta:
        ordering = ['-created_time']
# 然后数据迁移       
python manage.py makemigrations
python manage.py migrate

>>> paginator = Paginator(blogs, 10)
>>> paginator
<django.core.paginator.Paginator object at 0x1021de550>
>>> dir(paginator)
>> paginator.count
35
>>> paginator.num_pages
4
>>> page1 = paginator.page(1)
>>> page1
<Page 1 of 4>
>>> page1.object_list
```

## 14.优化分页展示

- 优化分页显示，提升用户体验
    - 不要显示太多页码选择，影响页面布局
    - 高亮显示当前页码
- 页码栏，优化显示的页码范围，这部分看似简单，内容不少

```python
current_page_num = page_of_blogs.number # 获取当前页码
# 获取当前页的前后2页的页码范围
page_range = [x for x in range(current_page_num - 2, current_page_num + 3) if x in paginator.page_range ]

# 加上省略号间隔页码
if page_range[0] - 1 >= 2:
    page_range.insert(0, '...')
if paginator.num_pages - page_range[-1] >= 2:
    page_range.append('...')
# 加上首页和尾页
if page_range[0] != 1:
    page_range.insert(0, 1)
if page_range[-1] != paginator.num_pages:
    page_range.append(paginator.num_pages)
```

- 公用全局设置放在setting中，统一管理
    - 引用`from django.conf import settings; settings.xxx`

- [分页组件](https://v3.bootcss.com/components/#pagination)

## 15.上下篇博客和按月分类

- 对比当前博客，得到上一篇或下一篇

```python
blog = get_object_or_404(Blog, pk=blog_pk)
context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
context['blog'] = blog
```

- `.objects.filter()` 筛选条件
    - 比较 `__gt` `__gte` `__lt` `__lte`
    - 包含 `__contains`
    - 开头是 `__startswith`
    - 结尾是 `__endswith`
    - `__in` `__range`

```python
>>> from blog.models import Blog
>>> Blog.objects.filter(title__contains='shell')
<QuerySet [<Blog: <Blog: shell 下第1篇>>]>
>>> Blog.objects.filter(title__startswith='shell')
<QuerySet [<Blog: <Blog: shell 下第1篇>>]>
>>> Blog.objects.filter(id__in=[1,2,3])
<QuerySet [<Blog: <Blog: 第一篇博客>>, <Blog: <Blog: 第二篇博客>>, <Blog: <Blog: 第三篇博客>>]>
>>> Blog.objects.filter(id__range=(1, 3))
<QuerySet [<Blog: <Blog: 第一篇博客>>, <Blog: <Blog: 第二篇博客>>, <Blog: <Blog: 第三篇博客>>]>
```

- `.objects.exclude()` 排出条件，和filter相反，都是得到查询QuerySet
- 加入双下划线筛选，用于
    - 字段查询类型
    - 外键拓展，以博客分类为例
    - 日期拓展，以按月份为例
    - 支持链式重新，可以一直链接下去
- 按日期查询 [.objects.dates()](https://docs.djangoproject.com/zh-hans/2.0/ref/models/querysets/#dates)
    - "month" returns a list of all distinct year/month values for the field.
    - `Blog.objects.dates('created_time', 'month', order='DESC')`
    - asc 按升序排列, desc 按降序排列

## 16.统计分类博客的数量

- 获取博客分类的对应博客数量
- 方法一，附加一个数量属性

```python
# 获取博客分类的对应博客数量
blog_types = BlogType.objects.all()
blog_types_list = []
for blog_type in blog_types:
    blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    blog_types_list.append(blog_type)

# context['blog_types'] = BlogType.objects.all()
context['blog_types'] = blog_types_list
```

- 方法二，使用annotate拓展查询字段，注释统计信息

```python
from django.db.models import Count

BlogType.objects.annotate(blog_count=Count('blog'))
context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
```

- 获取日期归档对应的博客数量

```py
blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
blog_dates_dict = {}
for blog_date in blog_dates:
    blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
    blog_dates_dict[blog_date] = blog_count 

context['blog_dates'] = blog_dates_dict
```

## 17.博客后台富文本编辑

- 使用html丰富页面
- 简单文本编辑 -》直接贴入html代码

```sh
{{ blog.content|safe }}  # 安全的，可以识别html tab
{{ blog.content|striptags|truncatechars:120 }} # 有时不用显示tag，过滤掉tag
```

- 富文本编辑 -》 最终解析成html，富文本编辑器、markdown编辑器
- 使用django-ckeditor, 选择标准
    - 具有基本的富文本编辑功能
    - 有持续更新维护
    - 可以查看源码
    - 可以上传图片
- 安装django-ckeditor [链接](https://pypi.org/project/django-ckeditor/)
    - `pip install django-ckeditor`
    - 注册应用`ckeditor`
    - 配置models, 把字段改成RichTextField
    - 执行数据库迁移，进后台编辑博客就可以看到
- 添加上传图片功能
    - `pip install pillow`
    - 注册应用`ckeditor_uploader`
    - 配置setting, media路径
    - 配置url
    - 配置model，把字段改成RichTextUploadingField

```py
# media 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 配置ckeditor
CKEDITOR_UPLOAD_PATH = 'upload/'

# urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from blog.views import blog_list
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('blog/', include('blog.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# models
from ckeditor_uploader.fields import RichTextUploadingField
content = RichTextUploadingField()
```

## 18.博客阅读简单计数

- 简单计数处理
    - Blog模型添加数字字段记录
    - 每次打开链接，记录+1

- 自定义计数规则， 怎样才算阅读一次
    - 无视是否同一个人，每次打开都记录，会造成刷阅读量，刷新即可
    - 若同一个人，间隔多久才算阅读1次
- 通过设置浏览器cookie计数，防止一人多次计数

```py
# 如果浏览器中没有设置的cookie了，就计数
if not request.COOKIES.get('blog_%s_readed' % blog_pk):
    blog.readed_num += 1
    blog.save()

response = render_to_response('blog/blog_detail.html', context)
# response.set_cookie('blog_%s_readed' % blog_pk, 'true', max_age=60) # 60s 失效
response.set_cookie('blog_%s_readed' % blog_pk, 'true') # 默认退出浏览器失效
return response
```

- COOKIES 计数方法的缺点
    - 后台编辑博客可能影响计数，而且计数的更新也会更新了博客的时间
    - 功能单一，无法统计某一天的阅读量

## 19.博客阅读计数优化

- 添加新的计数模型，计数功能独立，减少对原博客的影响
    - 计数字段  和  博客 通过 外键 关联

```py
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
    # 或者 blog = models.ForeignKey(Blog, on_delete=models.DO_NOTHING)

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'blog')

if not request.COOKIES.get('blog_%s_readed' % blog_pk):
    # blog.readed_num += 1
    # blog.save()

    if ReadNum.objects.filter(blog=blog):
        # 存在记录
        readnum = ReadNum.objects.get(blog=blog)
    else:
        # 不存在记录
        readnum = ReadNum(blog=blog)
    # 计数加1
    readnum.read_num += 1
    readnum.save()
```

- 创建专门用于计数的应用，独立出更加通用的计数功能，可以对任意模型计数
    - 计数： 关联哪个模型  +  对应主键值
    - [ContentType](https://docs.djangoproject.com/en/2.0/ref/contrib/contenttypes/)

- 创建专门用于计数的应用
    - `python manage.py startapp read_statistics`
- 添加计数 models

```py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

- 注册应用
- 数据迁移
- 添加后台管理

```py
from django.contrib import admin
from .models import ReadNum
# Register your models here.
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')
```

- 在Blog模型中引用添加ReadNum

```py
# shell 中实践 使用
>>> from read_statistics.models import ReadNum
>>> from blog.models import Blog
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.filter(model='blog')
<QuerySet [<ContentType: blog>]>
>>> ContentType.objects.get_for_model(Blog)
<ContentType: blog>
>>> ct = ContentType.objects.get_for_model(Blog)
>>> blog = Blog.objects.first()
>>> blog.pk
1
>>> ReadNum.objects.filter(content_type=ct, object_id=blog.pk)
<QuerySet [<ReadNum: ReadNum object (2)>]>
>>> rn = ReadNum.objects.filter(content_type=ct, object_id=blog.pk)[0]
>>> rn
<ReadNum: ReadNum object (2)>
>>> rn.read_num
11
```
