# '2018/8/16 11:03'
# coding=utf-8


from django.conf.urls import url
from blog import views

urlpatterns = [
    # 个人博客主站点
    url(r'^(\w+)/$', views.mysite),
    # 博客左侧分类栏
    url(r'^(\w+)/(category|tag|archive)/(.*)/$', views.mysite),
    # 文章详情
    url(r'^(\w+)/p/(\d+)/$', views.article)
]
