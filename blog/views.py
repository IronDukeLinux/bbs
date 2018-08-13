from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django import views
from blog.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from PIL import Image, ImageDraw, ImageFont  # 安装pip3 install pillow
import random
from io import BytesIO  # 对内存进行操作
# Create your views here.


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

    @staticmethod
    def get(request):
        return render(request, 'index.html')


# 专门用来返回验证码图片的视图
def v_code(request):
    # 生成随机图片
    # 生成随机颜色
    def random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    # 生成图片对象
    image_obj = Image.new(
        'RGB',  # 生成图片的模式
        # (250, 35),  # 图片大小
        (2500, 3500),  # 图片大小
        # random_color(),  # 图片颜色
        (255, 255, 255),  # 图片颜色
    )
    # 生成一个准备写字的画笔
    draw_obj = ImageDraw.Draw(image_obj)  # 在哪写
    font_obj = ImageFont.truetype('static/font/kumo.ttf', size=28)  # 加载本地的字体文件

    # 生成随机验证码
    # tmp = []
    # for i in range(5):
    #     n = str(random.randint(0, 9))
    #     u = chr(random.randint(65, 90))
    #     l = chr(random.randint(97, 122))
    #     r = random.choice([n, u, l])
    #     tmp.append(r)  # 生成的验证码保存起来用于和用户输入的对比
    #     # 每次生成的r写入图片
    #     draw_obj.text(
    #         (20+i*45, 0),  # 坐标
    #         r,  # 内容
    #         fill=random_color(),  # 颜色
    #         font=font_obj  # 字体
    #     )
    # 得到最终的验证码
    # v_code = ''.join(tmp)
    # 将该次请求的生成的验证码保存在该次请求对应的session数据中
    # request.session['v_code'] = v_code

    # 生成干扰线
    width = 2500  # 图片宽度（防止越界）
    height = 3500
    for i in range(5):
        # 第一个点的坐标
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        # 第二个点的坐标
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw_obj.line(
            (x1, y1, x2, y2),
            fill=random_color(),
        )

    # 生成干扰点
    for i in range(40):
        # draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x+400, y+400), 0, 90, fill=random_color())

    # 将生成的图片保存在内存中
    f = BytesIO()
    image_obj.save(f, 'png')
    # 从内存中读取数据
    data = f.getvalue()
    return HttpResponse(data, content_type='image/png')
