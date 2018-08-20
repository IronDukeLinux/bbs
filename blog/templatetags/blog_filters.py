# '2018/8/15 20:04'
# coding=utf-8


import random
from django import template
from blog import models
from django.db.models import Count
register = template.Library()


@register.filter
def che(value):
    return random.choice(value)


@register.inclusion_tag(filename='left_menu.html')
def left_menu(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    # 拿到用户关联的博客站点对象
    blog = user_obj.blog

    # 查找博客站点有哪些文章分类
    # category_list = models.Category.objects.filter(blog_id=blog.id)
    category_list = models.Category.objects.filter(blog=blog)

    # 查找博客站点有哪些文章标签
    # tag_list = models.Tag.objects.filter(blog_id=blog.id)
    tag_list = models.Tag.objects.filter(blog=blog)

    # 对当前blog的所有文章按照年月 分组 查询
    # 1。查询出当前作者写的所有文章
    # article_list = user_obj.article_set.all()
    # print('1', article_list)
    # 2。将所有查出的文章的创建时间格式化成年-月的格式，方便后续分组
    # article_list = article_list.extra(select={'y_m': 'DATE_FORMAT(create_time, "%%Y-%%m")'})
    # print('2', article_list)
    # 3。根据主y_m字段进行分组，统计每个分组的文章数
    # article_list = article_list.values('y_m').annotate(c=Count('id'))
    # print('3', article_list)
    # 4。把页面需要的日期归档和文章数量字段取出来
    # article_list = article_list.values('y_m', 'c')
    # print('4', article_list)
    archive_list = user_obj.article_set.all().extra(
        select={'y_m': 'DATE_FORMAT(create_time, "%%Y-%%m")'}
    ).values('y_m').annotate(c=Count('id'))
    color_list = ['primary', 'success', 'info', 'warning', 'danger']
    return {
        'username': username,
        'category_list': category_list,
        'tag_list': tag_list,
        'archive_list': archive_list,
        'color_list': color_list,
    }
