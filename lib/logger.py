import logging

class LoggingWrapper():
    def __init__(self):
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%Y/%m/%d %H:%M:%S %p"
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

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