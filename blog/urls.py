# '2018/8/16 11:03'
# coding=utf-8


from django.conf.urls import url
from blog import views

urlpatterns = [
    # 管理后台
    url(r'^backend/$', views.backend),
    # 添加文章页面
    url(r'^add_article/$', views.add_article),
    # 富文本编辑器的图片上传
    url(r'^upload/$', views.upload),
    # 删除文章
    url(r'^del_article/(\d+)', views.del_article),
    # 编辑文章
    url(r'^edi_article/(\d+)', views.edi_article),


    # 个人博客主站点
    url(r'^(\w+)/$', views.mysite),
    # 博客左侧分类栏
    url(r'^(\w+)/(category|tag|archive)/(.*)/$', views.mysite),
    # 文章详情
    url(r'^(\w+)/p/(\d+)/$', views.article)
]
