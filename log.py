import logging
from logging.handlers import TimedRotatingFileHandler
import time
import os

class Log_Recorder:
    def __init__(self):
        self.logger = self.get_logger()

    def get_logger(self):
        self.logger = logging.getLogger(__name__)
        # 日志格式
        formatter = logging.Formatter('[%(asctime)s-%(filename)s][%(funcName)s-%(lineno)d]--%(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        # 日志级别
        self.logger.setLevel(logging.DEBUG)
        # 控制台日志
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)
        # info日志文件名
        case_dir = r'./logs/'
        if not os.path.exists(case_dir):
            os.makedirs(case_dir)
        info_file_name = time.strftime("%Y-%m-%d") + '.log'
        info_handler = TimedRotatingFileHandler(filename=case_dir + info_file_name,
                                                when='MIDNIGHT',
                                                interval=1,
                                                backupCount=7,
                                                encoding='utf-8')
        info_handler.setFormatter(formatter)
        self.logger.addHandler(info_handler)
        return self.logger
