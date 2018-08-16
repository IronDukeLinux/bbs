from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django import views
from blog.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from PIL import Image, ImageDraw, ImageFont  # 安装pip3 install pillow
import random
from io import BytesIO  # 对内存进行操作
from django.views.decorators.cache import never_cache  # 告诉浏览器不要缓存数据
from utils.geetest import GeetestLib
from blog import models
from utils.mypage import MyPage
# Create your views here.


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 滑动验证码第一步的API,初始化一些参数用来校验滑动验证码
def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 滑动验证码版本的登录
def login2(request):
    res = {'code': 0}
    if request.method == "POST":
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 滑动验证码校验通过
            username = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                login(request, user)
            else:
                # 用户名或密码错误
                res['code'] = 1
                res['msg'] = '用户名或密码错误'
        else:
            # 滑动验证码校验失败
            res['code'] = 1
            res['msg'] = '怪物吃掉了拼图'
        return JsonResponse(res)
    form_obj = LoginForm()
    return render(request, 'login2.html', {'form_obj': form_obj})


# 登录
class Login(views.View):

    @staticmethod
    def get(request):
        form_obj = LoginForm()
        return render(request, 'login.html', {'form_obj': form_obj})

    def post(self, request):
        res = {'code': 0}
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        v_code = request.POST.get('v_code')
        # 判断验证码是否正确
        if v_code.upper() != request.session.get('v_code', '').upper():
            res['code'] = 1
            res['msg'] = '验证码错误'
        else:
            # 校验用户名密码是否正确
            user = authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                login(request, user)
            else:
                # 用户名或密码错误
                res['code'] = 1
                res['msg'] = '用户名或密码错误'
        return JsonResponse(res)


# 首页
class Index(views.View):

    def get(self, request):
        article_list = models.Article.objects.all()
        # 分页
        data_amount = article_list.count()
        page_num = request.GET.get('page', 1)
        page_obj = MyPage(page_num, data_amount, request.path_info, per_page=2)
        # 按照分页的设置对总数据进行切片
        data = article_list[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return render(request, 'index.html', {'article_list': data, 'page_html': page_html})


# 专门用来返回验证码图片的视图
# 返回响应的时候告诉浏览器不要缓存
@never_cache
def v_code(request):
    # 生成随机图片
    # 生成随机颜色
    def random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    # 生成图片对象
    image_obj = Image.new(
        'RGB',  # 生成图片的模式
        (250, 35),  # 图片大小
        # (2500, 3500),  # 图片大小
        random_color(),  # 图片颜色
        # (255, 255, 255),  # 图片颜色
    )
    # 生成一个准备写字的画笔
    draw_obj = ImageDraw.Draw(image_obj)  # 在哪写
    font_obj = ImageFont.truetype('static/font/kumo.ttf', size=28)  # 加载本地的字体文件

    # 生成随机验证码
    tmp = []
    for i in range(5):
        n = str(random.randint(0, 9))
        u = chr(random.randint(65, 90))
        l = chr(random.randint(97, 122))
        r = random.choice([n, u, l])
        tmp.append(r)  # 生成的验证码保存起来用于和用户输入的对比
        # 每次生成的r写入图片
        draw_obj.text(
            (20+i*45, 0),  # 坐标
            r,  # 内容
            fill=random_color(),  # 颜色
            font=font_obj  # 字体
        )
    # 得到最终的验证码
    v_code = ''.join(tmp)
    # 将该次请求的生成的验证码保存在该次请求对应的session数据中
    request.session['v_code'] = v_code

    # 生成干扰线
    # width = 2500  # 图片宽度（防止越界）
    # height = 3500
    # for i in range(5):
    #     # 第一个点的坐标
    #     x1 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     # 第二个点的坐标
    #     x2 = random.randint(0, width)
    #     y2 = random.randint(0, height)
    #     draw_obj.line(
    #         (x1, y1, x2, y2),
    #         fill=random_color(),
    #     )

    # 生成干扰点
    # for i in range(40):
    #     draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     定义外接矩形的左上角和右下角，
    #     起始角（0度为3点钟方法，x轴正向），结束角（顺时针计算），
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=random_color())  # 在第四象限的1/4圆弧
    #     draw_obj.arc((x, y, x+400, y+400), 0, -90, fill=random_color())  # 除去第一象限的3/4圆弧

    # 将生成的图片保存在内存中
    f = BytesIO()
    image_obj.save(f, 'png')
    # 从内存中读取数据
    data = f.getvalue()
    return HttpResponse(data, content_type='image/png')


# 注册
class RegView(views.View):

    @staticmethod
    def get(request):
        form_obj = RegisterForm()
        return render(request, 'register.html', {'form_obj': form_obj})

    def post(self, request):
        res = {'code': 0}
        form_obj = RegisterForm(request.POST)
        # 使用form做校验
        if form_obj.is_valid():
            # 数据有效，注册用户
            # 注意移除不需要的re_password
            form_obj.cleaned_data.pop('re_password')
            # 拿到用户上传的头像文件
            avatar_file = request.FILES.get('avatar')
            # 直接将拿到的文件对象传给avatar字段就可以完成写文件，和将文件路径存入数据库的操作
            # 前提ORM定义的字段得是FileField，这是ORM的功能，和mysql数据库无关
            models.UserInfo.objects.create_superuser(**form_obj.cleaned_data, avatar=avatar_file)
            # 登录成功之后跳转到登录页面
            res['msg'] = '/login/'
        else:
            # 用户的数据有问题
            res['code'] = 1
            res['msg'] = form_obj.errors
        return JsonResponse(res)


# 注销
def logout2(request):
    logout(request)
    return redirect('/login/')


# 用户站点
def mysite(request):
    ironduke1234 = models.UserInfo.objects.get(username='ironduke1234')
    color_list = ['primary', 'success', 'info', 'warning', 'danger']
    return render(request, 'mysite.html', {'ironduke1234': ironduke1234, 'color_list': color_list})
