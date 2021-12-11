from django.contrib.sessions.backends.db import SessionStore
SessionUserId = 'userId'
# 获取request的session字典
def GetSessionObj(request) -> dict:
    return request.session