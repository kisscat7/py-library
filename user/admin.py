from django.contrib import admin
from user.models import User
from user.models import RealName


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('UserName', 'Account', 'Tel', 'RealNameAuthentication')
    fields = ['UserName', 'Tel','Status','RealNameAuthentication']


admin.site.site_title = '图书馆'
admin.site.site_header = "图书馆管理后台"
admin.site.index_title = '管理后台'