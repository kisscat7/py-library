TelLen = 11

UsernameLen = 40

IdentifyIdLen = 18

PasswordLenMax = 16
PasswordLenMin = 8

AccountLenMax = 18
AccountLenMin = 6

ISBNLen = 13


# 手机号合法性检查 Create By Wf@2021.11.30
def checkTelValidity(telStr: str) -> bool:
    """
        手机号规则
        长度：11位数字
    """
    # 长度检查
    strLen = len(telStr)
    if strLen != TelLen:
        # log.Error('长度异常')
        return False
    if not telStr.isdigit():
        # log.Error('字符非法')
        return False
    return True


# 用户名合法性检查 Create By Wf@2021.11.30
def checkUserNameValidity(userName: str) -> bool:
    """
        用户名规则
        长度：25位字符
        不得含有非法字符
    """
    # 长度检查
    strLen = len(userName)
    if strLen > UsernameLen:
        # log.Error('长度异常')
        return False
    for word in BadWords:
        if word in userName:
            # log.Debug('违禁词')
            return False
    return True


BadWords = [
    '恐怖'
    '主席'
    '特朗普'
]


# 身份证号法性检查 Create By Wf@2021.11.30
def checkIdentifyIdLenValidity(identifyId: str) -> bool:
    """
        用户名规则
        长度：25位字符
        不得含有非法字符
    """
    # 长度检查
    idLen = len(identifyId)
    if idLen != IdentifyIdLen:
        # log.Error('长度异常')
        return False
    if not identifyId[:-1].isdigit():
        # log.Error('身份证号不合规')
        return False
    if not (identifyId[-1:].isdigit() or identifyId[:-1] == 'X'):
        return False
    return True


# 账号合法性检查 Create By Wf@2021.11.29
def checkAccountValidity(account: str) -> bool:
    """
        账号规则
        长度：6~18
        包饭字符：英文字母、数字、下划线
        首尾限制：英文字母开头
    """
    # 长度检查
    accountLen = len(account)
    if accountLen < AccountLenMin or accountLen > AccountLenMax:
        # log.Error('长度异常')
        return False
    # 首字符检查
    if not account[0].isalpha():
        # log.Error('首字母非字母')
        return False
    # 检查字符
    for s in account:
        if not (s.isdigit() or s.isalpha() or s == '_'):
            # log.Error('非法字符')
            return False
    return True


# 密码合法性检查 Create By Wf@2021.11.29
def checkPasswordValidity(password: str) -> bool:
    """
        密码规则
        长度：8-16
        包饭字符：英文字母、数字、特殊符号等
    """
    # 长度检查
    passwordLen = len(password)
    if passwordLen < PasswordLenMin or passwordLen > PasswordLenMax:
        # log.Error('长度异常')
        return False
    return True


# 检查ISBN编号合法性 Create By wf@2021.12.5
def CheckISBNValidity(ISBNStr: str):
    if not ISBNStr.isdigit():
        return False
    return len(ISBNStr) == ISBNLen
