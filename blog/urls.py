# '2018/8/16 11:03'
# coding=utf-8


from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^(\w+)/$', views.mysite),
    url(r'^(\w+)/(category|tag|archive)/(.*)/$', views.mysite),
]
