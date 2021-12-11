from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Index, name="book_index"),# 主页
    path('search', views.Search, name="book_search"),# 搜索
    re_path('book-(\d+)', views.BookDetails, name="book_details"),# 书籍详情
    re_path('borrowBook-(\d+)', views.BorrowBook, name="book_borrow"),# 书籍详情
    re_path('returnBook-(\d+)', views.ReturnBook, name="book_return"),# 书籍详情
]