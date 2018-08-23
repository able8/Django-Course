from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadNum, ReadDetail


def read_statistics_one_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.pk)  # cookie key

    if not request.COOKIES.get(key):

        # 总阅读量 + 1
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            # 不存在记录
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        # 计数加1
        readnum.read_num += 1
        readnum.save()

        # 每天阅读量 + 1
        date = timezone.now().date()
        if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
            # 存在记录
            readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
        else:
            # 不存在记录
            readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
        # 计数加1
        readDetail.read_num += 1
        readDetail.save() 
    return key
