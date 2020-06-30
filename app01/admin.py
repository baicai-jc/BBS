from django.contrib import admin
from app01 import models

# Register your models here.
admin.site.register(models.UserInfo)    # 注册的表名会默认加个后缀s,如果想自定义可以在models.py中在类中定义
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.Article2Tag)
admin.site.register(models.UpAndDown)
admin.site.register(models.Comment)
