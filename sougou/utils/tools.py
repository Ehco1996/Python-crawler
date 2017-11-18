import os
import time
import logging

class UtilLogger(object):

    '''
    建立日志文件，并以特定格式输出日志
    Args:
        name:logger名字
        logfile_name 日志文件名
        level:调试级别，日志中只打印高于此级别的日志，例如logging.DEBUG、logging.info，此级别可以在set_level函数里设置
    '''
    def __init__(self, name, logfile_name=None, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
        ch = None
        if logfile_name is None:
            ch = logging.StreamHandler()
        else:
            logDir = os.path.dirname(logfile_name)
            if logDir != "" and not os.path.exists(logDir):
                os.mkdir(logDir)
                pass
            now = time.localtime()
            suffix = '.%d%02d%02d' % (now.tm_year, now.tm_mon, now.tm_mday)
            ch = logging.FileHandler(logfile_name+suffix)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def set_level(self,level):
        '''
        设置调试等级
        Args:
            level，字符串，可选debug、info、warning、error
        '''
        if level.lower() == "debug":
            self.logger.setLevel(logging.DEBUG)
        elif level.lower() == "info":
            self.logger.setLevel(logging.INFO)
        elif level.lower() == "warning":
            self.logger.setLevel(logging.WARNING)
        elif level.lower() == "error":
            self.logger.setLevel(logging.ERROR)

    def debug(self, message):
        '''
        打印函数，最低调试级别的打印，
        Args:
            message为要打印的信息
        info/warn/error函数与此类似
        '''
        self.logger.debug(message)

    def info(self,message):
	    self.logger.info(message)

    def warn(self,message):
	    self.logger.warn(message)

    def error(self,message):
	    self.logger.error(message)


# def test():
#     log = UtilLogger('testname','test')
#     log.set_level('info')
#     log.debug('++++++++++++++')
#     log.info('--------------')
#     log.warn('==============')
#     log.error('_____________')
# if __name__ == '__main__':
#     test()
