from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest
import datetime
import pytz
from user.models import User
from books.models import Book
from books.models import BookRecord
from books.models import Book
from config import log
from tool.check import *
from tool.session import *
from tool.struct import *


# Create your views here.
def Index(request: WSGIRequest):
    BookRecord(
        BookId=1,
        UserId=1,
        BorrowTime=datetime.datetime.now(),
        PredictReturnTime=datetime.datetime.now(),
        Status=0,
    ).save()
    session = GetSessionObj(request)
    if SessionUserId not in session.keys():
        # 有session 定位到图书馆主页
        return render(request, 'books/index.html')
    context = request.context
    if session.get(SessionUserId) is not None:
        userObj = User.LoadById(session.get(SessionUserId))
        context[ContextUserData] = userObj.GetLoginStruct()
    return render(request, 'books/index.html', context)


# 搜索 Create By wf@2021.12.3
def Search(request: WSGIRequest):
    session = GetSessionObj(request)
    context = request.context
    if SessionUserId in session.keys():
        # 用户登陆状态下自动打包信息
        userObj = User.LoadById(session.get(SessionUserId))
        context[ContextUserData] = userObj.GetLoginStruct()
    keywords = request.GET.get('keyword').strip()
    context['keyword'] = keywords
    # 判断keyword类型（书名、作者、ISBN）
    bookMap = {}
    # ISBN 编号检索
    bookListByISBN = Book.GetBooksByISBN(keywords)
    for bookObj in bookListByISBN:
        bookMap[bookObj.Id] = bookObj
    # 书名检索
    bookListByName = Book.GetBooksByBookName(keywords)
    for bookObj in bookListByName:
        bookMap[bookObj.Id] = bookObj
    # 作者检索

    bookListByAuthor = Book.GetBooksByAuthor(keywords)
    for bookObj in bookListByAuthor:
        bookMap[bookObj.Id] = bookObj

    if len(bookMap) < 1:
        context[ContextError] = '无相关书籍'
        return render(request, 'books/index.html', context)
    context[ContextSearchBookData] = bookMap.values()
    return render(request, 'books/search.html', context)


# 书籍详情 Create By wf@2021.12.6
def BookDetails(request: WSGIRequest, bookIdStr: str):
    bookId = int(bookIdStr.strip())
    bookObj = Book.GetBooksById(bookId)
    if bookObj is None:
        return redirect(reverse('book_index'))
    session = GetSessionObj(request)
    context = request.context
    context['borrow'] = True
    if SessionUserId in session.keys():
        # 用户登陆状态下自动打包信息
        userObj = User.LoadById(session.get(SessionUserId))
        context[ContextUserData] = userObj.GetLoginStruct()
        context[ContextBookData] = bookObj
        brList = BookRecord.GetBorrowingList(bookId=bookId, userId=userObj.id)
        if len(brList) > 0:
            context['borrow'] = False
    return render(request, 'books/details.html', context)


# 借书 Create By wf@2021.12.6
def BorrowBook(request: WSGIRequest, bookIdStr: str):
    session = GetSessionObj(request)
    context = request.context
    if SessionUserId not in session.keys():
        context[ContextError] = '请先登录！'
        return render(request, 'gateway/login.html', context)
    userObj = User.LoadById(session.get(SessionUserId))
    if userObj is None:
        context[ContextError] = '用户异常，请重新登录'
        return render(request, 'gateway/login.html', context)
    context[ContextUserData] = userObj.GetLoginStruct()

    bookId = int(bookIdStr.strip())
    bookObj = Book.GetBooksById(bookId)
    if bookObj is None:
        context[ContextError] = '书籍不存在！'
        return render(request, 'books/index.html', context)
    context[ContextBookData] = bookObj
    brList = BookRecord.GetBorrowingList(bookId=bookId, userId=userObj.id)
    if len(brList) > 0:
        context[ContextError] = '不能重复借阅'
        context['borrow'] = False
        return render(request, 'books/details.html', context)
    if not bookObj.Offset(-1):
        context[ContextError] = '借阅失败'
        context['borrow'] = True
        return render(request, 'books/details.html', context)
    if len(BookRecord.GetUserBorrowingList(userObj.id)) > 5:
        context[ContextError] = '已达借阅上限（没人最多同时借阅5本数）'
        return render(request, 'books/details.html', context)
    nowTime = datetime.datetime.now()
    endTime = nowTime + datetime.timedelta(days=15)
    BookRecord(
        BookId=1,
        UserId=1,
        BorrowTime=nowTime,
        PredictReturnTime=endTime,
        Status=0,
    ).save()
    return redirect(reverse('user_index'))


# 还书 Create By wf@2021.12.6
def ReturnBook(request: WSGIRequest, bookIdStr: str):
    context = request.context
    session = GetSessionObj(request)
    if SessionUserId not in session.keys():
        context[ContextError] = '请先登录！'
        return render(request, 'gateway/login.html', context)
    userObj = User.LoadById(session.get(SessionUserId))
    if userObj is None:
        context[ContextError] = '用户异常，请重新登录'
        return render(request, 'gateway/login.html', context)
    context[ContextUserData] = userObj.GetLoginStruct()
    bookId = int(bookIdStr.strip())
    bookObj = Book.GetBooksById(bookId)
    if bookObj is None:
        context[ContextError] = '书籍不存在！'
        return render(request, 'books/index.html', context)
    context[ContextBookData] = bookObj
    brList = BookRecord.GetBorrowingList(bookId=bookId, userId=userObj.id)
    if len(brList) < 1:
        context[ContextError] = '您未借阅该书籍'
        return redirect(reverse('user_index'))
    bookRecord = brList[0]
    if not bookObj.Offset(1):
        context[ContextError] = '归还失败'
        return redirect(reverse('user_index'))
    bookRecord.Status = 1
    bookRecord.PredictReturnTime = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
    bookRecord.save()
    return redirect(reverse('user_index'))
