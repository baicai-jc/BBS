from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser

# Create your models here.
'''
先写普通字段
之后在写外键字段
'''

class UserInfo(AbstractUser):
    phone = models.BigIntegerField(null=True,blank=True,verbose_name="手机号")
    """
    null=True   数据库该字段可以为空
    blank=True  admin后台管理该字段可以为空
    """
    # 头像
    avatar = models.FileField(upload_to="avatar/",default='avatar/default.png')
    """
    给avatar字段传文件对象 该文件会自动存储到avatar文件夹 然后avatar字段只保存文件路径avatar/default.png
    """
    create_time = models.DateTimeField(auto_now_add=True)

    blog = models.OneToOneField(to='Blog',null=True)
    class Meta:
        verbose_name_plural = "用户表"
        # verbose_name = "用户表"     # 使用verbose_name更改还是会加s ==> 用户表s

    def __str__(self):
        return self.username

class Blog(models.Model):
    site_name = models.CharField(max_length=32,verbose_name='站点名称')
    site_title = models.CharField(max_length=32,verbose_name='站点标题')
    # 简单模拟 认识样式内部原理的操作
    site_theme = models.CharField(max_length=64,verbose_name='站点样式')  # 存css/js的文件路径

    class Meta:
        verbose_name_plural = "站点表"

    def __str__(self):
        return self.site_name

class Category(models.Model):
    name = models.CharField(max_length=32,verbose_name='文章分类')
    blog = models.ForeignKey(to='Blog',null=True)

    class Meta:
        verbose_name_plural = "文章分类表"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=32,verbose_name='文章标签')
    blog = models.ForeignKey(to='Blog',null=True)

    class Meta:
        verbose_name_plural = "文章标签表"

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=64,verbose_name='文章标题')
    desc = models.CharField(max_length=255,verbose_name='文章简介')
    # 文章内容有很多 一般情况下都是使用TextField
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(auto_now_add=True)

    # 数据库字段设计优化
    up_num = models.BigIntegerField(default=0,verbose_name='点赞数')
    down_num = models.BigIntegerField(default=0,verbose_name='点踩数')
    comment_num = models.BigIntegerField(default=0,verbose_name='评论数')

    # 外键字段
    blog = models.ForeignKey(to='Blog',null=True)
    category = models.ForeignKey(to='Category',null=True)
    tags = models.ManyToManyField(to='Tag',
                                  through='Article2Tag',
                                  through_fields=('article','tag')
                                  )

    class Meta:
        verbose_name_plural = "文章表"

    def __str__(self):
        return self.title

class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')

    class Meta:
        verbose_name_plural = "文章&标签关联表"

class UpAndDown(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    is_up = models.BooleanField() # 传布尔值存0/1

    class Meta:
        verbose_name_plural = "点赞点踩表"

class Comment(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    content = models.CharField(max_length=255,verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    # 自关联
    parent = models.ForeignKey(to='self',null=True)  # 一定要加null=True,因为有些评论就是根评论

    class Meta:
        verbose_name_plural = "评论表"




