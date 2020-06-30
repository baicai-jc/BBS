from django import template
from app01 import models
from django.db.models import Count
from django.db.models.functions import TruncMonth
register = template.Library()

# 自定义inclusion_tag
@register.inclusion_tag('left_menu.html')
def left_menu(username):

    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    # 查询当前用户所有的分类以及分类下的文章数
    category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count("article__pk")).values_list(
        'name', 'count_num', "pk")
    # print(category_list)

    # 查询当前用户所有的标签以及标签下的文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count("article__pk")).values_list('name',
                                                                                                         'count_num',
                                                                                                         "pk")

    # 按照年月统计所有的文章
    date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values(
        "month").annotate(count_num=Count("pk")).values_list('month', 'count_num')
    return locals()