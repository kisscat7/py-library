from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest
from tool.session import *
from tool.struct import *
from tool.check import *
from config import log
from user.models import User


# from books.views import


# Create your views here.
def Register(request: WSGIRequest):
    session = GetSessionObj(request)
    if SessionUserId in session.keys():
        # 有session 定位到图书馆主页
        return redirect(reverse('book_index'))
    # 页面请求
    if request.method != "POST":
        return render(request, 'gateway/register.html')
    '''注册请求'''
    # 获取传递给模板的数据
    context = request.context
    # 数据获取
    tel = request.POST.get('tel')  # 获取注册手机号
    account = request.POST.get('account')  # 获取账号
    userName = request.POST.get('username')  # 获取用户名
    password = request.POST.get('password')  # 获取密码
    affirmPassword = request.POST.get('affirmPassword')  # 获取确认密码 - 第二次输入密码
    context['registerBakData'] = {
        'tel': tel,
        'account': account,
        'username': userName,
        'password': password,
        'affirmPassword': affirmPassword
    }
    # 检查手机号字符串合法
    if not checkTelValidity(tel):
        context[ContextError] = '手机号不合规范'
        context['registerBakData']['tel'] = ''
        return render(request, 'gateway/register.html', context)
    # 检查手机号是否已被注册
    userObj: User = User.LoadByTel(tel)
    if userObj is not None:
        context[ContextError] = '手机号已被注册'
        context['registerBakData']['tel'] = ''
        return render(request, 'gateway/register.html', context=context)
    # 检查账号字符串合法性
    if not checkAccountValidity(account):
        context[ContextError] = '账号不合规范'
        context['registerBakData']['account'] = ''
        return render(request, 'gateway/register.html', context=context)
    # 检查账号存在
    userObj: User = User.LoadByAccount(account)
    if userObj is not None:
        context[ContextError] = '用户名已被占用'
        context['registerBakData']['account'] = ''
        return render(request, 'gateway/register.html', context=context)
    # 用户名检查
    if not checkUserNameValidity(userName):
        context[ContextError] = '用户名不合规'
        context['registerBakData']['username'] = ''
        return render(request, 'gateway/register.html', context)
    # 密码格式检查
    if not checkPasswordValidity(password):
        context[ContextError] = '密码格式不合规'
        context['registerBakData']['password'] = ''
        context['registerBakData']['affirmPassword'] = ''
        return render(request, 'gateway/register.html', context=context)
    # 密码一致性比对
    if password != affirmPassword:
        context[ContextError] = '密码不一致'
        context['registerBakData']['affirmPassword'] = ''
        return render(request, 'gateway/register.html', context=context)
    # 用户保存入库
    userObj: User = User.CreateUser(
        tel=tel,
        account=account,
        username=userName,
        password=password
    )
    log.Debug('注册成功', userObj.id, userObj.UserName)
    return redirect(reverse('gateway_login'))


# 登录 Create By Wf@2021.11.27
def Login(request: WSGIRequest):
    session: dict = GetSessionObj(request)
    if SessionUserId in session.keys():
        # 有session 定位到图书馆主页
        return redirect(reverse('book_index'))
    # 页面请求
    if request.method != "POST":
        return render(request, 'gateway/login.html')
    '''登陆请求'''
    # 获取传递给模板的数据
    context = request.context
    # 获取账号
    account = request.POST.get('account')
    # 检查账号字符串合法性
    if not checkAccountValidity(account):
        context[ContextError] = '账号异常'
        return render(request, 'gateway/login.html', context=context)
    # 检查账号存在
    userObj: User = User.LoadByAccount(account)
    if userObj is None:
        context[ContextError] = '用户不存在'
        return render(request, 'gateway/login.html', context=context)
    # 获取密码
    password = request.POST.get('password')
    # 检查密码字符串合法性
    if not checkPasswordValidity(password):
        context[ContextError] = '密码长度不正确'
        return render(request, 'gateway/login.html', context=context)
    # 检查密码正确与否
    if not userObj.CheckPassword(password):
        context[ContextError] = '密码不正确'
        return render(request, 'gateway/login.html', context=context)
    # 登录正常导出登录信息
    context[ContextUserData] = userObj.GetLoginStruct()
    log.Debug('登录成功', userObj.id, userObj.UserName)
    session[SessionUserId] = userObj.id
    return redirect(reverse('book_index'))


def Exit(request: WSGIRequest):
    request.session.flush()
    return redirect(reverse('gateway_login'))