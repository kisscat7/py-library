from django.db import models
import hashlib
# Create your models here.
from config import log

ContextLoginTel = 'tel'
ContextLoginAccount = 'account'
ContextLoginUserName = 'username'
ContextLoginReal = 'real'

AccountStatusNormal = 0  # 账号状态：正常
AccountStatusWarning = 1  # 账号状态：异常-警告
AccountStatusBanned = 2  # 账号状态：封禁


# User 用户实体类
class User(models.Model):

    """用户基本信息属性
        Tel                         ：用户手机号
        UserName                    ：用户用户名
        Password                    ：用户密码
        Status                      ：账号状态
        RealNameAuthentication      ：用户实名认证状态
    """
    class Meta:
        verbose_name_plural = '用户基本信息'
    # Id = models.IntegerField(primary_key=True, verbose_name='主键玩家id')
    Tel = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    Account = models.CharField(max_length=18, unique=True, default='', verbose_name='账户')
    UserName = models.CharField(max_length=40, unique=True, verbose_name='用户名')
    Password = models.CharField(max_length=200, verbose_name='MD5加密密码')
    Status = models.SmallIntegerField(default=0, verbose_name='账号状态', choices=((0, '正常'), (1, '异常'),))
    RealNameAuthentication = models.BooleanField(default=False, verbose_name='实名认证状态')

    # 实例方法：检查字符串是否和User密码匹配
    def CheckPassword(self, password: str) -> bool:
        return self.Password == self.GetPasswordMD5(password)

    # 获取登录结构体
    def GetLoginStruct(self) -> dict:
        return {
            ContextLoginTel: self.Tel,
            ContextLoginAccount: self.Account,
            ContextLoginUserName: self.UserName,
            ContextLoginReal: self.RealNameAuthentication
        }

    # 静态方法：字符串md5加密
    @staticmethod
    def GetPasswordMD5(password: str) -> str:
        return hashlib.md5(password.encode()).hexdigest()

    # 类方法：根据account加载指定User
    @classmethod
    def LoadByAccount(cls, account: str):
        try:
            o = cls.objects.get(Account=account)
            return o
        except User.DoesNotExist:
            return None

    # 类方法：根据Tel加载指定User
    @classmethod
    def LoadByTel(cls, tel: str):
        try:
            o = cls.objects.get(Tel=tel)
            return o
        except User.DoesNotExist:
            return None

    # 类方法：根据id加载指定User
    @classmethod
    def LoadById(cls, userId: int):
        try:
            o = cls.objects.get(id=userId)
            return o
        except User.DoesNotExist:
            return None
        except Exception as e:
            log.Error(e)
            return None

    # 类方法：新建用户
    @classmethod
    def CreateUser(cls, tel: str, account: str, username: str, password: str):
        newUserObj = User(
            Tel=tel,
            Account=account,
            UserName=username,
            Password=hashlib.md5(password.encode()).hexdigest(),
            Status=AccountStatusNormal,
            RealNameAuthentication=False,
        )
        newUserObj.save()
        return newUserObj

    def __str__(self):
        return self.UserName


# RealName 用户实名认证
class RealName(models.Model):
    class Meta:
        verbose_name_plural = '实名认证信息'
    UserId = models.IntegerField(primary_key=True, verbose_name='主键玩家id')
    Name = models.CharField(max_length=100, verbose_name='真实姓名')
    IdentifyId = models.CharField(max_length=18, verbose_name='身份证号')

    @classmethod
    def LoadByUserId(cls, userId: int):
        try:
            o = cls.objects.get(UserId=userId)
            return o
        except RealName.DoesNotExist:
            return None

    def __str__(self):
        return self.Name
