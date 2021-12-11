from django.db import models
from django.db import transaction
from django.utils import timezone
import os


def save_image(instance, filename):
    return os.path.join('static', 'img', filename)


# Create your models here.
# Book 书基本信息
class Book(models.Model):
    class Meta:
        verbose_name_plural = '书籍信息'

    Id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    BookName = models.CharField(max_length=200, verbose_name='书名')
    Author = models.CharField(max_length=200, default='', verbose_name='作者')
    ISBN = models.CharField(max_length=13, default='', verbose_name='ISBN编号')
    BookCover = models.ImageField(upload_to=save_image, default='static/img/img.jpg', verbose_name='书籍封面')
    Publish = models.CharField(max_length=200, default='', verbose_name='出版社')
    Description = models.TextField(default='', verbose_name='简介')
    Number = models.IntegerField(default=0, verbose_name='书籍数量')

    def __str__(self):
        return '%s' % {
            'Id': self.Id,
            'BookName': self.BookName,
            'ISBN': self.ISBN,
            'Publish': self.Publish,
            'Description': self.Description,
            'Number': self.Number
        }

    @transaction.atomic
    def Offset(self, num: int) -> bool:
        if self.Number + num < 0:
            return False
        self.Number += num
        self.save()
        return True

    @classmethod
    def GetBooksById(cls, ID: int):
        try:
            o = cls.objects.get(Id=ID)
            return o
        except Book.DoesNotExist:
            return None

    @classmethod
    def GetBooksByISBN(cls, ISBNStr: str) -> list:
        return cls.objects.filter(ISBN__icontains=ISBNStr)

    @classmethod
    def GetBooksByBookName(cls, BookName: str):
        return cls.objects.filter(BookName__icontains=BookName)

    @classmethod
    def GetBooksByAuthor(cls, AuthorStr: str):
        return cls.objects.filter(Author__icontains=AuthorStr)


# 借阅记录
class BookRecord(models.Model):
    BookId = models.IntegerField(primary_key=True, verbose_name='图书ID')
    UserId = models.IntegerField(verbose_name='使用者id')
    BorrowTime = models.DateTimeField(default=timezone.now, verbose_name='借出时间')
    PredictReturnTime = models.DateTimeField(default=timezone.now, verbose_name='还书时间')
    Status = models.IntegerField(default=0, verbose_name='状态', choices=((-1, '已超时'), (0, '借出中 '), (1, '已归还'),))

    @classmethod
    def GetBorrowingList(cls, bookId: int, userId: int):
        return cls.objects.filter(BookId=bookId, UserId=userId, Status__lt=1)

    @classmethod
    def GetUserBorrowingList(cls, userId: int):
        return cls.objects.filter(UserId=userId, Status__lt=1)

    @classmethod
    def GetUserAllRecordList(cls, userId: int):
        return cls.objects.filter(UserId=userId)
