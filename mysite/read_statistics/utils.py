import datetime
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadNum, ReadDetail


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
    read_nums = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        read_details = ReadDetail.objects.filter(
            content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))  # 聚合
        read_nums.append(result['read_num_sum'] or 0) # 空则为0
    return read_nums
