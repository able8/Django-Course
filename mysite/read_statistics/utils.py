import datetime
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadNum, ReadDetail
from blog.models import Blog


def read_statistics_one_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.pk)  # cookie key

    if not request.COOKIES.get(key):
        # 总阅读量 + 1
        readnum, created = ReadNum.objects.get_or_create(
            content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 每天阅读量 + 1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(
            content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key


# 统计最近7天阅读量
def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(
            content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))  # 聚合
        read_nums.append(result['read_num_sum'] or 0)  # 空则为0
    return dates, read_nums


# 获取今日热门文章
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(
        content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]  # 取前7条


# 获取昨天热门文章
def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(
        content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]


# 获取7天热门文章
def get_7_days_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects\
        .filter(read_details__date__lt=today, read_details__date__gte=date)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs[:7]
