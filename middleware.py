from django.utils.deprecation import MiddlewareMixin
from tool.struct import *
from config import log


class MyMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    # @staticmethod
    def process_request(self, request):
        request.context = GetDataStruct()

    # @staticmethod
    def process_response(self, request, response):
        log.Debug("Response Request: ", request.context, seg=' ')
        return response
