import datetime

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.core.handlers.wsgi import WSGIRequest
from user.models import User
from user.models import RealName
from books.models import Book
from books.models import BookRecord
import hashlib
import pytz
from config import log
from tool.session import *
from tool.struct import *
from tool.check import *


# Create your views here.
# 个人信息主页 Create By Wf@2021.11.30
def Index(request: WSGIRequest):
    session = GetSessionObj(request)
    if SessionUserId not in session.keys():
        return redirect(reverse('gateway_login'))
    context = request.context
    userObj = User.LoadById(session.get(SessionUserId))
    context[ContextUserData] = userObj.GetLoginStruct()
    # 打包数据
    bookList = []
    recordList = []
    now = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
    for r in BookRecord.GetUserAllRecordList(userObj.id):
        bookObj = Book.GetBooksById(r.BookId)
        if now > r.PredictReturnTime and r.Status == 0:
            r.Status = -1
            r.save()
        if bookObj is None:
            continue
        if r.Status < 1:
            bookList.append({
                'BookId': r.BookId,
                'BookName': bookObj.BookName,
                'Author': bookObj.Author,
                'ISBN': bookObj.ISBN,
                'Publish': bookObj.Publish,
                'StartTime': r.BorrowTime,
                'EndTime': r.PredictReturnTime,
                'Status': r.Status
            })
        recordList.append({
            'BookId': r.BookId,
            'BookName': bookObj.BookName,
            'Author': bookObj.Author,
            'ISBN': bookObj.ISBN,
            'Publish': bookObj.Publish,
            'StartTime': r.BorrowTime,
            'EndTime': r.PredictReturnTime,
            'Status': r.Status
        })
    context[ContextUserBookRack] = bookList
    context[ContextUserRecords] = recordList
    return render(request, 'user/index.html', context)


# 基本信息修改接口 Create By Wf@2021.11.30
def SetData(request: WSGIRequest):
    session = GetSessionObj(request)
    if SessionUserId not in session.keys():
        log.Debug(session.keys())
        return redirect(reverse('gateway_login'))
    context = request.context
    userObj = User.LoadById(session.get(SessionUserId))
    if request.method != 'POST':
        context[ContextUserData] = userObj.GetLoginStruct()
        return render(request, 'user/index.html', context)
    isUpdate = False
    tel = request.POST.get('tel')
    if tel != userObj.Tel:
        if not checkTelValidity(tel):
            context[ContextError] = '手机号不合规'
            context[ContextUserData] = userObj.GetLoginStruct()
            return render(request, 'user/index.html', context)
        userObj.Tel = tel
        isUpdate = True
    username = request.POST.get('username')
    if username != userObj.UserName:
        if not checkUserNameValidity(username):
            context[ContextError] = '用户名不合规'
            context[ContextUserData] = userObj.GetLoginStruct()
            return render(request, 'user/index.html', context)
        userObj.UserName = username
        isUpdate = True
    if isUpdate:
        userObj.save()
    context[ContextUserData] = userObj.GetLoginStruct()
    return render(request, 'user/index.html', context)


# 实名认证 Create By Wf@2021.11.30
def RealNameAuthentication(request: WSGIRequest):
    session = GetSessionObj(request)
    if SessionUserId not in session.keys():
        return redirect(reverse('gateway_login'))
    context = request.context
    userObj = User.LoadById(session.get(SessionUserId))
    # 检查是否重复认证
    if userObj.RealNameAuthentication:
        return redirect(reverse('user_index'))
    # 检查是否是已验证
    if RealName.LoadByUserId(userObj.id) is not None:
        userObj.RealNameAuthentication = True
        userObj.save()
        return redirect(reverse('user_index'))
    if request.method != 'POST':
        return redirect(reverse('user_index'))
    # 获取真实姓名
    realName = request.POST.get('name')
    # 获取身份证号
    identifyId = request.POST.get('identityId')
    # 身份证号检查
    if not checkIdentifyIdLenValidity(identifyId):
        context[ContextUserData] = userObj.GetLoginStruct()
        context[ContextError] = '身份证号异常'
        return render(request, 'user/index.html', context)
    userObj.RealNameAuthentication = True
    userObj.save()

    RealName(
        UserId=userObj.id,
        Name=realName,
        IdentifyId=identifyId
    ).save()
    return redirect(reverse('user_index'))


# 修改密码 Create By wf@2021.12.3
def ResetPassword(request: WSGIRequest):
    session = GetSessionObj(request)
    if SessionUserId not in session.keys():
        return redirect(reverse('gateway_login'))
    context = request.context
    userObj = User.LoadById(session.get(SessionUserId))
    if userObj is None:
        return redirect(reverse('gateway_login'))
    password = request.POST.get('password')
    confirmPassword = request.POST.get('confirm_password')
    if not checkPasswordValidity(password):
        context[ContextError] = '密码不合规'
        context[ContextUserData] = userObj.GetLoginStruct()
        return render(request, 'user/index.html', context)
    if password != confirmPassword:
        context[ContextError] = '密码不一致'
        context[ContextUserData] = userObj.GetLoginStruct()
        return render(request, 'user/index.html', context)
    userObj.Password = hashlib.md5(password.encode()).hexdigest()
    userObj.save()
    log.Debug('密码修改成功')
    return redirect(reverse('user_index'))
