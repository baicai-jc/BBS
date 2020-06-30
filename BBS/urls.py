"""BBS URL Configuration

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
from app01 import views
from django.views.static import serve
from BBS import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 注册
    url(r'^register/', views.register,name='register'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 退出登陆
    url(r'^logout/', views.logout, name='logout'),
    # 图片验证码
    url(r'^get_code/', views.get_code, name='get_code'),
    # 首页
    url(r'^home/', views.home, name='home'),
    # 修改密码
    url(r'^set_password/', views.set_password, name='set_password'),
    # 点赞点踩
    url(r'^up_or_down/', views.up_or_down),
    # 文章评论
    url(r'^comment/', views.comment),
    # 后台管理
    url(r'^backend/', views.backend,name="backend"),
    # 添加文章
    url(r'^add/article/', views.add_article, name="add_article"),
    # 删除文章
    url(r'^del/article/', views.del_article, name="del_article"),
    # 编辑器上传图片接口
    url(r'^upload_img/', views.upload_img, name="upload_img"),
    # 修改头像
    url(r'^set/avatar/', views.set_avatar, name="set_avatar"),

    # 暴露后端指定文件夹资源
    url(r'^files/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    # 个人站点
    url(r'^(?P<username>\w+)/$', views.site, name='site'),

    # 编辑文章
    url(r'^(?P<username>\w+)/edit_article/(?P<article_id>\d+)', views.edit_article, name="edit_article"),
    # 删除文章
    url(r'^(?P<username>\w+)/del_article/(?P<article_id>\d+)', views.del_article, name="del_article"),

    # 侧边栏筛选功能    让多个url指向同一个视图函数
    # url(r'^(?P<username>\w+)/category/(\d+)',views.site),
    # url(r'^(?P<username>\w+)/tag/(\d+)',views.site),
    # url(r'^(?P<username>\w+)/archive/(\w+)',views.site),
    # 上面三条合并
    url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)',views.site),

    # 文章详情页
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)',views.article_detail),


]
