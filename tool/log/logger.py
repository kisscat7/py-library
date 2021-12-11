import logging
import time
import os
import sys
import shutil

LOG_FORMAT = "[%(asctime)s]: %(message)s"  # \" %(levelname)-8s ▶ %(message)s"


class Log(object):
    _instance = None

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    def __init__(self, loggerName: str):
        if 'runserver' not in sys.argv:
            self.status = False
            return
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个用于写入日志文件的handler，
        self.logFileName = loggerName + ' - ' + getTimeStrDoFileName() + '.log'
        fileHandler = logging.FileHandler(self.logFileName, 'a', encoding='utf-8')
        fileHandler.setLevel(logging.DEBUG)
        # 创建一个用于控制台输出的handler，
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        # 创建日志输出模板
        formatObj = logging.Formatter(LOG_FORMAT)
        fileHandler.setFormatter(formatObj)
        consoleHandler.setFormatter(formatObj)
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        fileHandler.close()
        consoleHandler.close()
        self.Info("The model of Log is Ready ! The Log File Name is %s !" % self.logFileName)
        self.status = True

    def Debug(self, *param, seg = ', '):
        try:
            raise Exception
        except:
            import sys
            f = sys.exc_info()[2].tb_frame.f_back
        mStr = "\"" + str(f.f_code.co_filename) + ":" + str(f.f_lineno) + "\"" + \
               " %s ▶ %s" % ('Debug', seg.join(["%s" % s for s in param]))
        self.logger.debug(mStr)

    def Info(self, *param, seg = ', '):
        try:
            raise Exception
        except:
            import sys
            f = sys.exc_info()[2].tb_frame.f_back
        mStr = "\"" + str(f.f_code.co_filename) + ":" + str(f.f_lineno) + "\"" + \
               " %s ▶ %s" % ('Debug', seg.join(["%s" % s for s in param]))
        self.logger.info(mStr)

    def Warning(self, *param, seg = ', '):
        try:
            raise Exception
        except:
            import sys
            f = sys.exc_info()[2].tb_frame.f_back
        mStr = "\"" + str(f.f_code.co_filename) + ":" + str(f.f_lineno) + "\"" + \
               " %s ▶ %s" % ('Debug', seg.join(["%s" % s for s in param]))
        self.logger.warning(mStr)

    def Error(self, *param, seg = ', '):
        try:
            raise Exception
        except:
            import sys
            f = sys.exc_info()[2].tb_frame.f_back
        mStr = "\"" + str(f.f_code.co_filename) + ":" + str(f.f_lineno) + "\"" + \
               " %s ▶ %s" % ('Debug', seg.join(["%s" % s for s in param]))
        self.logger.error(mStr)

    def Critical(self, *param, seg = ', '):
        try:
            raise Exception
        except:
            import sys
            f = sys.exc_info()[2].tb_frame.f_back
        mStr = "\"" + str(f.f_code.co_filename) + ":" + str(f.f_lineno) + "\"" + \
               " %s ▶ %s" % ('Debug', seg.join(["%s" % s for s in param]))
        self.logger.critical(mStr)

    def LogFileClean(self):
        if not self.status:
            return
        path = os.getcwd()
        for fr in os.listdir(path):
            absolutePath = os.path.join(path, fr)
            if self.logFileName == fr:
                continue

            bakPath = os.path.join(path, "bak\log")
            if not os.path.exists(bakPath):
                os.makedirs(bakPath)
            if absolutePath[-4:] == '.log':
                shutil.move(absolutePath, os.path.join(bakPath, fr))

    @classmethod
    def NewLog(cls, loggerName: str):
        return Log(loggerName)

    @classmethod
    def GetLogger(cls, name=''):
        if cls._instance is None:
            cls._instance = cls.NewLog(name)
            cls._instance.LogFileClean()
        return cls._instance


def getTimeStrDoFileName() -> str:
    timeFileStr = ''
    timeNow = time.localtime(time.time())
    len(str(timeNow.tm_year)) - 4
    timeFileStr += '0' * (4 - len(str(timeNow.tm_year))) + str(timeNow.tm_year) + '_'
    timeFileStr += '0' * (2 - len(str(timeNow.tm_mon))) + str(timeNow.tm_mon) + '_'
    timeFileStr += '0' * (2 - len(str(timeNow.tm_mday))) + str(timeNow.tm_mday) + '-'
    timeFileStr += '0' * (2 - len(str(timeNow.tm_hour))) + str(timeNow.tm_hour) + '_'
    timeFileStr += '0' * (2 - len(str(timeNow.tm_min))) + str(timeNow.tm_min) + '_'
    timeFileStr += '0' * (2 - len(str(timeNow.tm_sec))) + str(timeNow.tm_sec)
    return timeFileStr
