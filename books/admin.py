from django.contrib import admin
from books.models import Book


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('BookName', 'Author', 'ISBN', 'Publish', 'Number')
    fields = ['BookName', 'Author', 'ISBN', 'BookCover', 'Publish', 'Description', 'Number']
