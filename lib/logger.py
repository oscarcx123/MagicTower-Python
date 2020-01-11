import logging
import sysconf

class LoggingWrapper():
    def __init__(self):
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%Y/%m/%d %H:%M:%S %p"
        logging_level = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        if sysconf.LOGGING_LEVEL in logging_level:
            logging.basicConfig(level=logging_level[sysconf.LOGGING_LEVEL], format=LOG_FORMAT, datefmt=DATE_FORMAT)
        else:
            print("日志等级设置错误，启用默认配置！")
            logging.basicConfig(level=logging_level["ERROR"], format=LOG_FORMAT, datefmt=DATE_FORMAT)

    def debug(self, module_name, text):
        self.logger = logging.getLogger(module_name)
        self.logger.debug(text)

    def info(self, module_name, text):
        self.logger = logging.getLogger(module_name)
        self.logger.info(text)

    def warning(self, module_name, text):
        self.logger = logging.getLogger(module_name)
        self.logger.warning(text)

    def error(self, module_name, text):
        self.logger = logging.getLogger(module_name)
        self.logger.error(text)

    def critical(self, module_name, text):
        self.logger = logging.getLogger(module_name)
        self.logger.critical(text)