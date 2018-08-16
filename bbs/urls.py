"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.Login.as_view()),
    url(r'^login2/$', views.login2),  # 滑动验证码
    url(r'^pcgetcaptcha/$', views.pcgetcaptcha),  # 生成滑动验证码的初始数据
    url(r'^index/', views.Index.as_view()),
    url(r'^v-code/$', views.v_code),  # 验证码

    url(r'^reg/$', views.RegView.as_view()),  # 注册
    url(r'^logout/$', views.logout2),

    # 给用户上传文件 配置一个处理的路由
    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),

    # 用户的博客站点
    url(r'^ironduke1234/', views.mysite),
]
