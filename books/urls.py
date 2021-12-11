from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Index, name="book_index"),# ��ҳ
    path('search', views.Search, name="book_search"),# ����
    re_path('book-(\d+)', views.BookDetails, name="book_details"),# �鼮����
    re_path('borrowBook-(\d+)', views.BorrowBook, name="book_borrow"),# �鼮����
    re_path('returnBook-(\d+)', views.ReturnBook, name="book_return"),# �鼮����
]