from django.urls import path
from . import views

urlpatterns = [
    path('index', views.Index, name="user_index"),  # 个人主页
    path('setUserData', views.SetData, name="user_setData"),  # 个人信息修改
    path('realName', views.RealNameAuthentication, name="user_realName"),  # 实名认证
    path('resetPassword', views.ResetPassword, name="user_resetPassword"),  # 重置密码
]
