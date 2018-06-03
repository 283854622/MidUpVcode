from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from MidUpVcode.settings import BLACK_LIST, VIP_LIST

'''
所有的钩子函数都可以返回一个Response
一旦钩子函数返回了Response,整个请求的受理就结束了
'''


#继承于框架中的中间件
class MyAppMiddleware(MiddlewareMixin):

    #中间件的初始化方法，全局执行一次
    # def __init__(self):
    #     super(MyAppMiddleware,self).__init__()
    #     print('>>>>>>>>>>MyAppMiddleware __init__')

    #下钩子于所有路由被交给路由表之前
    def process_request(self,request):

        #获取客户端IP地址
        clientIp=request.META['REMOTE_ADDR']

        #请求的路由
        url=request.path
        print('>>>>>>>>>> process_request',request,clientIp,request.path)

        #屏蔽黑名单用户
        #只要客户端IP在黑名单中
        if clientIp in BLACK_LIST:
            #直接渲染fuckoff.html并立刻返回
            return render(request,'fuckoff.html')

        #当vip用户访问福利页面是提供更好的服务
        if clientIp in VIP_LIST and url == '/myapp/fuli/':
            return render(request, 'fuli.html', context={'imgpath': 'meinv2.jpg'})

        #福利页必须登录了才能查看
        if url == '/myapp/fuli/' and not request.session.get('uname',None):
            return redirect(reverse('myapp:login'))


    #下钩子于所有路由被交给路由表之前
    def process_view(self,requset,view_func,view_args,view_kwargs):
        print('>>>>>>>>>> process_view',requset,view_func,view_args,view_kwargs)


    #理论上下钩子于所有路由请求的模板被渲染完成以后
    #这个函数实测无法回调
    def process_template_response(self,request,response):
        print('>>>>>>>>>> process_template_response',request,response)
        return response

    # 下钩子于所有路由的响应被返回之前
    def process_response(self,requset,response):
        print('>>>>>>>>>> process_response',requset,response)
        return response

    def process_exception(self,request,exception):
        print('>>>>>>>>>> process_exception',request,exception)
        return redirect(reverse('/'))