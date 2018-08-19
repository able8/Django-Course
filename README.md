# Django_Course
Python Django Web开发  入门到实践 视频地址：https://space.bilibili.com/252028233/#/

看视频整理要点笔记

## 1 什么是Django
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

## 2 入门 Hello World
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
    
## 03. Django基本应用结构
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

