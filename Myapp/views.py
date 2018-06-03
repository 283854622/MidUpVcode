import os

import io
import random
import string

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from MidUpVcode.settings import BASE_DIR, MEDIA_ROOT, STATIC_URL
from Myapp.models import User


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        uname = request.POST.get('uname', None)
        upwd = request.POST.get('upwd', None)

        #获取用户输入的验证码
        vcode = request.POST.get('vcode', None)

        #拿到用户上传的文件数据，类型是框架类InMemoryUploadedFile
        uiconFile = request.FILES.get('uicon', None)

        # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
        print(uname, upwd, vcode, uiconFile, type(uiconFile))
        # f=InMemoryUploadedFile()

        # 手动存储上传的文件、
        #自定义文件位置
        fp = os.path.join(MEDIA_ROOT, 'x-' + uiconFile.name)

        #写入文件
        with open(fp, 'wb')as file:

            #逐'桶'读取上传的文件数据，并写入本地文件
            for buffer in uiconFile.chunks():
                file.write(buffer)

        # 校验验证码
        # 从session中获取正确的验证码
        sessVcode = request.session.get('vcode', None)

        # 比较用户输入的验证码与正确的验证码是否匹配
        #事先全部转换为大小写，这样用户可以忽略大小写
        if vcode and sessVcode and vcode.lower() == sessVcode.lower():

            user = User()
            user.uname = uname
            user.upwd = upwd

            #将上传过来的文件直接赋值给用户的ImageField字段uicon
            #框架会自动将图片存储在MEDIA_ROOT中
            if uiconFile:
                user.uicon = uiconFile
                user.save()

            return HttpResponse('注册成功')
        else:
            return HttpResponse('注册失败')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uname = request.POST.get('uname', None)
        upwd = request.POST.get('upwd', None)
        vcode = request.POST.get('vcode', None)

        # 校验验证码
        sessVcode = request.session.get('vcode', None)
        if vcode and sessVcode and vcode.lower() == sessVcode.lower():
            user = User.objects.filter(uname=uname).first()
            if user and upwd == user.upwd:
                request.session['uname'] = user.uname
                request.session['uicon'] = user.uicon.name

                return redirect(reverse('myapp:mine'))
            else:
                return HttpResponse('登录失败')
        else:
            return HttpResponse('登录失败')


def logout(request):
    return None


def mine(request):
    uname = request.session.get('uname', None)
    uicon = request.session.get('uicon', None)
    if uname:
        data = {
            'uname': uname,
            'uiconpath': STATIC_URL + 'uploads/' + uicon,
            'uiconfp': 'uploads/' + uicon,
        }
        return render(request, 'mine.html', context=data)
    else:
        return redirect(reverse('myapp:login'))


def fuli(request):
    print(5 / 0)
    return render(request, 'fuli.html', context={'imgpath': 'dj.jpg'})


def lottery(request):
    return None


def fuckoff(request):
    return None


'''
生成并返回验证码
'''


def getvcode(request):
    # 随机生成验证码
    # 设置生成大小写字母加数字的属性
    population = string.ascii_letters + string.digits
    # 随机生成4个大小写字母加数字
    letterlist = random.sample(population, 4)
    # 将生成的列表[a,A,1,2]用空字符''连接成字符串(aA12)
    vcode = ''.join(letterlist)

    # 保存该用户的验证码
    request.session['vcode'] = vcode

    # 绘制验证码
    # 创建画布（'RGB'格式，（宽157，高50），随机颜色）
    image = Image.new('RGB', (157, 50), color=getRandomColor())
    # 创建画布的画笔
    draw = ImageDraw.Draw(image)
    # 绘制文字
    # 设置字体样式的路径
    path = os.path.join(BASE_DIR, 'static', 'fonts', 'ADOBEARABIC-BOLDITALIC.OTF')
    # 设置字体样式
    font = ImageFont.truetype(font=path, size=40)

    # 根据生成的字符串长度遍历字符串的每个字符
    for i in range(len(vcode)):
        # 绘制文字（设置开始的位置（xy）,字符串的每个字符，颜色，字体样式）
        draw.text((20 + 30 * i, 5), vcode[i], fill=getRandomColor(), font=font)

    # 添加噪声
    # 设置噪点的最大个数
    for i in range(200):
        # 设置噪点的位子（xy）
        position = (random.randint(0, 157), random.randint(0, 50))
        # 画噪点（位置（xy）,颜色）
        draw.point(position, fill=getRandomColor())

    # 返回验证码
    # 删除画笔
    del draw
    # 创建字节容器
    buffer = io.BytesIO()
    # 将画布内容丢入容器,保存画布到容器中，设置格式为'png'
    image.save(buffer, 'png')
    # 返回容器内的字节,内容为容器中值，类型为图片/png格式
    return HttpResponse(content=buffer.getvalue(), content_type='image/png')


# 创建随机生成的颜色（'RGB'）
def getRandomColor():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return (red, green, blue)
