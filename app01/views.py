from django.shortcuts import render, HttpResponse, redirect
from app01.myforms import MyRegForm
from app01 import models
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import F
from app01.utils.mypage import Pagination
from app01.utils.photo_code import create_validate_code
from bs4 import BeautifulSoup
from BBS import settings

import json
import os


# Create your views here.
# 注册
def register(request):
    form_obj = MyRegForm()
    if request.method == "POST":
        back_dic = {"code": 1000, "msg": ""}
        # 校验数据是否合法
        form_obj = MyRegForm(request.POST)
        if form_obj.is_valid():
            # print(form_obj.cleaned_data)     # {'username': 'alias', 'password': '123', 'confirm_password': '123', 'email': '123@qq.com'}
            clean_data = form_obj.cleaned_data  # 将校验通过的数据字典赋值给一个变量
            clean_data.pop("confirm_password")  # {'username': 'alias', 'password': '123', 'email': '123@qq.com'}
            # 用户头像
            file_obj = request.FILES.get("avatar")
            """针对用户头像一定要判断是否传值 不能直接添加到字典中"""
            if file_obj:
                clean_data['avatar'] = file_obj
            # 操作数据库保存数据
            models.UserInfo.objects.create_user(**clean_data)
            back_dic["url"] = "/login/"
        else:
            back_dic["code"] = 2000
            back_dic["msg"] = form_obj.errors
        return JsonResponse(back_dic)

    return render(request, "register.html", locals())


# 登录
def login(request):
    if request.is_ajax():
        if request.method == "POST":
            back_dic = {"code": 1000, "msg": ""}
            username = request.POST.get("username")
            password = request.POST.get("password")
            code = request.POST.get("code")
            # 校验验证码是否正确    自己决定是否忽略验证码大小写    统一转大写或小写即可
            if request.session.get("code").lower() == code.lower():
                # 校验用户名和密码

                user_obj = auth.authenticate(request, username=username, password=password)
                if user_obj:
                    # 保存用户状态
                    auth.login(request, user_obj)
                    back_dic["url"] = '/home/'
                    print(request.user, type(request.user))
                else:
                    back_dic["code"] = 2000
                    back_dic["msg"] = "用户名或密码错误"
            else:
                back_dic["code"] = 3000
                back_dic["msg"] = "验证码错误"

            return JsonResponse(back_dic)
    return render(request, 'login.html')


# 退出登录
@login_required
def logout(request):
    auth.logout(request)
    return redirect("/home/")


"""
图片相关的模块
    # pip3 install pillow
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

"""
Image:生成图片
ImageDraw:能够在图片上乱涂乱画
ImageFont:控制字体样式
ImageFilter:控制图片模糊度
"""
from io import BytesIO, StringIO

"""
内存管理器模块
BytesIO：临时的帮你存储数据 返回的时候数据就是二进制格式
StringIO：临时的帮你存储数据 返回的时候数据就是字符串格式
"""

import random


def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_code(request):
    # 推导步骤1：直接获取后端现成的图片二进制数据发送给前端
    # with open(r"static/img/111.jpg", "rb") as f:
    #     data = f.read()
    # return HttpResponse(data)
    #
    # 推导步骤2：利用pillow模块动态产生图片（文件存储繁琐IO操作效率低）
    # img_obj = Image.new('RGB', (430, 35), "red")   # 第二个参数图片尺寸(要和前端划定的尺寸一致),第三个参数还可以放三基色参数
    # img_obj = Image.new('RGB', (430, 35), get_random())
    # 先将图片对象保存起来
    # with open("xxx.png",'wb') as f:
    #     img_obj.save(f,"png")   # 文件句柄，图片格式
    # # 再将图片对象读取出来
    # with open('xxx.png','rb') as f:
    #     data = f.read()
    # return HttpResponse(data)

    # 推导步骤3：借助于内存管理模块
    # img_obj = Image.new('RGB', (430, 35), get_random())
    # io_obj = BytesIO()  # 生成一个内存管理器对象，可以看成是文件句柄
    # img_obj.save(io_obj,'png')     # 要指定图片的格式
    # return HttpResponse(io_obj.getvalue())    # io_obj.getvalue()读取出文件，返回的是二进制格式

    # 最终步骤：绘制图片验证码
    # img_obj = Image.new('RGB', (430, 35), get_random())
    # img_draw = ImageDraw.Draw(img_obj)  # 产生一个画笔对象
    # img_font = ImageFont.truetype("static/font/222.TTF", 30)  # 字体样式,以及字体大小
    #
    # # 随机验证码  五位数的随机验证码 数字 小写字母 大写字母
    # code = ''
    # for i in range(5):
    #     random_upper = chr(random.randint(65, 90))
    #     random_lower = chr(random.randint(97, 122))
    #     random_int = str(random.randint(0, 9))
    #     # 从上面三个里面随机选一个
    #     tmp = random.choice([random_upper, random_lower, random_int])
    #     # 将产生的随机字符串写入图片
    #     """
    #     为什么一个个写而不是生成好了之后再写
    #     因为一个个写能够控制每个字体的间隙 而生成好之后再写的话
    #     间隙就没法控制了
    #     """
    #     img_draw.text((i * 45 + 100, -3), tmp, get_random(), img_font)
    #     # 拼接随机字符串
    #     code += tmp
    # print(code)
    # # 随机验证码在登录的视图函数中需要用到 要比对，所以要找地方存起来且其他视图函数也能拿到（可以放在auth_session表中）
    # request.session['code'] = code
    # io_obj = BytesIO()
    # # img_obj = img_obj.filter(ImageFilter.GaussianBlur)
    # img_obj.save(io_obj, "png")
    #
    # return HttpResponse(io_obj.getvalue())

    # ============================================

    f = BytesIO()  # 创建一个内存地址存放图片
    img, code = create_validate_code()  # 调用方法生成图片对象和验证码
    request.session['code'] = code  # 设置session
    print(code)
    img.save(f, 'PNG')  # 保存图片
    return HttpResponse(f.getvalue())  # 返回图片


# 首页
def home(request):
    # 查询本网站所有的文章数据，展示到前端页面
    article_queryset = models.Article.objects.all()
    form_obj = MyRegForm()
    return render(request, "home.html", locals())


# 修改密码
@login_required
def set_password(request):
    if request.is_ajax():
        if request.method == "POST":
            back_dic = {"code": 1000, "msg": ""}
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            is_right = request.user.check_password(old_password)
            if is_right:
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    back_dic["msg"] = "修改成功"
                else:
                    back_dic["code"] = 2000
                    back_dic["msg"] = "两次密码不一致"
            else:
                back_dic["code"] = 3000
                back_dic["msg"] = "原密码错误"
            return JsonResponse(back_dic)


def site(request, username, **kwargs):
    """
    :param request:
    :param username:
    :param kwargs: 如果该参数有值 也就意味着需要对article_list做额外的筛选
    :return:
    """
    # 先校验当前用户名对应的个人站点是否存在
    user_obj = models.UserInfo.objects.filter(username=username).first()
    # 如果用户不存在，返回404页面
    if not user_obj:
        return render(request, "errors.html")
    blog = user_obj.blog
    # 查询当前个人站点的所有文章,并展示到个人站点页面
    article_list = models.Article.objects.filter(blog=blog)  # 侧边栏的筛选其实就是对article_list再进一步筛选

    if kwargs:
        # print(kwargs)  # {'condition': 'tag', 'param': '1'}
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        # 判断用户到底想按照哪个条件筛选数据
        if condition == 'category':
            article_list = article_list.filter(category_id=param)
        elif condition == 'tag':
            article_list = article_list.filter(tags__id=param)
        else:
            year, month = param.split('-')  # 2020-11  [2020,11]
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

    # # 查询当前用户所有的分类以及分类下的文章数
    # category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count("article__pk")).values_list('name','count_num',"pk")
    # # print(category_list)
    #
    # # 查询当前用户所有的标签以及标签下的文章数
    # tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count("article__pk")).values_list('name','count_num',"pk")
    #
    # # 按照年月统计所有的文章
    # date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values("month").annotate(count_num=Count("pk")).values_list('month','count_num')
    return render(request, "site.html", locals())


# 文章详情
def article_detail(request, username, article_id):
    """
    :param request:
    :param username:
    :param article_id:
    :return:
    """
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog

    # 获取文章对象
    article_obj = models.Article.objects.filter(pk=article_id, blog__userinfo__username=username).first()

    if not article_obj:
        return render(request, "errors.html")
    # 获取当前 文章所有的评论内容
    comment_list = models.Comment.objects.filter(article=article_obj)
    return render(request, "article_detail.html", locals())


# 点赞点踩
def up_or_down(request):
    """
    1.校验用户是否登录
    2.判断当前文章是否是当前用户自己写的（自己不能给自己的文章点赞）
    3.当前用户是否已经给当前文章点过赞或点踩
    :param request:
    :return:
    """
    if request.is_ajax():
        back_dic = {"code": 1000, "msg": ""}
        # 判断当前用户是否登录
        if request.user.is_authenticated():
            article_id = request.POST.get("article_id")
            is_up = request.POST.get("is_up")  # 得到的是字符串格式布尔值true,false
            is_up = json.loads(is_up)
            # 判断当前文章是否是当前用户自己写的（自己不能给自己的文章点赞）
            article_obj = models.Article.objects.filter(pk=article_id).first()
            if not article_obj.blog.userinfo == request.user:
                # 校验当前用户是否已经给当前文章点过赞或点踩
                is_click = models.UpAndDown.objects.filter(user=request.user, article=article_obj)
                if not is_click:
                    # 操作数据库 记录数据
                    # 判断当前用户点了赞还是踩，从而决定给哪个字段加
                    if is_up:
                        # 给点赞数加一
                        models.Article.objects.filter(pk=article_id).update(up_num=F("up_num") + 1)
                        back_dic["msg"] = "点赞成功"
                    else:
                        # 给点踩数加一
                        models.Article.objects.filter(pk=article_id).update(down_num=F("down_num") + 1)
                        back_dic["msg"] = "点踩成功"
                    # 操作点赞点踩表
                    models.UpAndDown.objects.create(user=request.user, article=article_obj, is_up=is_up)
                else:
                    back_dic["code"] = 1001
                    back_dic["msg"] = "你已经点过了，不能再点了"
            else:
                back_dic["code"] = 1002
                back_dic["msg"] = "自己不能给自己点赞或点踩"
        else:
            back_dic["code"] = 1003
            back_dic["msg"] = "请先<a href='/login/'>登录</a>"
        return JsonResponse(back_dic)


from django.db import transaction


def comment(request):
    # 自己也可以给自己的文章评论
    if request.is_ajax():
        if request.method == "POST":
            back_dic = {"code": 1000, "msg": ""}
            if request.user.is_authenticated():
                article_id = request.POST.get("article_id")
                content = request.POST.get("content")
                parent_id = request.POST.get("parent_id")
                # 直接操作评论表 存储数据   两张表 Article&Comment
                with transaction.atomic():
                    models.Article.objects.filter(pk=article_id).update(comment_num=F("comment_num") + 1)
                    models.Comment.objects.create(user=request.user, article_id=article_id, content=content,
                                                  parent_id=parent_id)
                back_dic["msg"] = "评论成功"

            else:
                back_dic["code"] = 1001
                back_dic["msg"] = "用户未登录"
        return JsonResponse(back_dic)


@login_required
def backend(request):
    # 获取当前用户对象所有的文章展示到页面
    article_list = models.Article.objects.filter(blog=request.user.blog)
    current_page = request.GET.get('page', 1)  # 如果获取不到当前页码 就展示第一页
    all_count = article_list.count()

    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=10)
    page_queryset = article_list[page_obj.start:page_obj.end]
    return render(request, "backend/backend.html", locals())


@login_required
def add_article(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")
        tag_id_list = request.POST.getlist("tag")
        # beautifulsoup4 模块使用
        soup = BeautifulSoup(content, "html.parser")
        tags = soup.find_all()
        # 获取所有的标签
        for tag in tags:
            # print(tag.name)  # 获取页面上所有标签
            # 针对script标签 直接删除
            if tag.name == "script":
                # 删除标签
                tag.decompose()

        # 文章简介
        # 截取文本
        # desc = content[0:150]
        desc = soup.text[0:150]
        article_obj = models.Article.objects.create(
            title=title,
            content=str(soup),
            desc=desc,
            category_id=category_id,
            blog=request.user.blog
        )
        # 文章和标签表的关系表是我们用半自动方式创建的，不能使用add set remove clear方法
        # 自己去操作关系表
        # 批量插入
        article_obj_list = []
        for i in tag_id_list:
            article_obj_list.append(models.Article2Tag(article=article_obj, tag_id=i))

        models.Article2Tag.objects.bulk_create(article_obj_list)
        # 跳转到后台管理文章的展示页
        return redirect("backend")

    category_list = models.Category.objects.filter(blog=request.user.blog)
    tag_list = models.Tag.objects.filter(blog=request.user.blog)

    return render(request, "backend/add_article.html", locals())


# 后台编辑文章
@login_required
def edit_article(request, username, article_id):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")
        tag_id_list = request.POST.getlist("tag")
        # beautifulsoup4 模块使用
        soup = BeautifulSoup(content, "html.parser")
        tags = soup.find_all()
        # 获取所有的标签
        for tag in tags:
            # print(tag.name)  # 获取页面上所有标签
            # 针对script标签 直接删除
            if tag.name == "script":
                # 删除标签
                tag.decompose()

        # 文章简介
        # 截取文本
        # desc = content[0:150]
        desc = soup.text[0:150]
        article_obj = models.Article.objects.filter(pk=article_id).update(
            title=title,
            content=str(soup),
            desc=desc,
            category_id=category_id,
            blog=request.user.blog
        )
        # 文章和标签表的关系表是我们用半自动方式创建的，不能使用add set remove clear方法
        # 自己去操作关系表
        # 更新
        edit_article_obj =  models.Article.objects.filter(pk=article_id).first()
        edit_article_obj.tags.clear()
        article_obj_list = []
        for i in tag_id_list:
            article_obj_list.append(models.Article2Tag(article=edit_article_obj, tag_id=i))

        models.Article2Tag.objects.bulk_create(article_obj_list)
        return redirect("backend")

    category_list = models.Category.objects.filter(blog=request.user.blog)
    tag_list = models.Tag.objects.filter(blog=request.user.blog)
    article_obj = models.Article.objects.filter(pk=article_id).first()

    return render(request, 'backend/edit_article.html', locals())

# 删除文章
def del_article(request,username, article_id):
    edit_article_obj = models.Article.objects.filter(pk=article_id).first()
    edit_article_obj.tags.clear()
    models.Article.objects.filter(pk=article_id).delete()

    return redirect("backend")


def upload_img(request):
    """
    //成功时
    {
            "error" : 0,
            "url" : "http://www.example.com/path/to/file.ext"
    }
    //失败时
    {
            "error" : 1,
            "message" : "错误信息"
    }
    :param request:
    :return:
    """
    back_dic = {"error": 0}

    if request.method == "POST":
        # 获取用户后端编辑上传的图片
        # print(request.FILES)   # 打印看到键imgFile
        file_obj = request.FILES.get("imgFile")
        file_dir = os.path.join(settings.BASE_DIR, 'files', 'article_img')

        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        # 拼接图片完整路径
        file_path = os.path.join(file_dir, file_obj.name)

        # 保存文件
        with open(file_path, 'wb') as f:
            for line in file_obj:
                f.write(line)

        back_dic['url'] = '/files/article_img/%s' % file_obj.name

    return JsonResponse(back_dic)


@login_required
def set_avatar(request):
    if request.method == "POST":
        file_obj = request.FILES.get('avatar')
        # print(file_obj.name)
        # # 修改头像方法一
        # file_path = 'avatar/%s' % file_obj
        # # 保存文件
        # with open("files/%s" %file_path, 'wb') as f:
        #     for line in file_obj:
        #         f.write(line)
        #
        # models.UserInfo.objects.filter(pk=request.user.pk).update(avatar=file_path)

        # 修改头像方法二
        user_obj = request.user
        user_obj.avatar = file_obj
        user_obj.save()
        return redirect('/home/')

    blog = request.user.blog
    username = request.user.username
    return render(request, "set_avatar.html", locals())
