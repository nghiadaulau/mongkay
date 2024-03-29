import datetime
import uuid
import logging

from applications.core.settings import settings


class LogMessage(object):
    def __init__(self, logger=None, func_name="", user="", client_id="", trace_id=None, service_name=None):
        self._logger = self.get_logger(logger)
        self.func_name = func_name
        self.user = user
        self.client_id = client_id
        self.tracer = None
        self.span = None
        self.trace_id = uuid.uuid1().hex if not trace_id else trace_id
        self.service_name = service_name if service_name else settings.SERVICE_NAME

    def set_user_log(self, username):
        """
        :param username: this username will be shown in each log line.
        :return:
        """
        self.user = username

    @property
    def pub_logger(self):
        """
        :return: logger object
        """
        return self._logger

    @staticmethod
    def get_logger(logger=None):
        """
        :param logger: logger name
        :return: logger object
        """
        if isinstance(logger, (logging.Logger, logging.RootLogger)):
            return logger
        else:
            logger = logging.getLogger("" if not logger else logger)
            return logger

    @staticmethod
    def logs_message(level, message, logger_obj):
        """
        :param level: level to log
        :param message: message to log
        :param logger_obj: log adapter
        :return:
        """
        level = level.upper()
        logger_level = {
            'CRITICAL': 50,
            'ERROR': 40,
            'WARNING': 30,
            'INFO': 20,
            'DEBUG': 10,
            'NOTSET': 0
        }
        logger_obj.log(logger_level.get(level), message)

    def log(self, lv, message, func_name="", ):
        """
        :param lv: level to log
        :param message: message to log
        :param func_name: function name where we wrote log line
        :return:
        """
        log_message = {
            'func_name': self.func_name if not func_name else func_name,
            'message': message,
            'user': self.user,
            "traceback": "trace-id-{}".format(self.trace_id),
            "time": f"{datetime.datetime.now()}"
        }

        my_adapter = logging.LoggerAdapter(self._logger,
                                           {
                                               'func_name': self.func_name if not func_name else func_name,
                                               'user': self.user,
                                               "traceback": "trace-id-{}".format(self.trace_id),
                                               "time": f"{datetime.datetime.now()}"
                                           })
        self.logs_message(lv, log_message, my_adapter)

    def info(self, message, func_name=""):
        """
        :param message: message to log
        :param func_name: function name where we wrote log line
        :return:
        """
        self.log("info", message, func_name)

    def error(self, message, func_name=""):
        """
        :param message: message to log
        :param func_name: function name where we wrote log line
        :return:
        """
        self.log("error", message, func_name)

    def warning(self, message, func_name=""):
        """
        :param message: message to log
        :param func_name: function name where we wrote log line
        :return:
        """
        self.log("warning", message, func_name)

    def debug(self, message, func_name=""):
        """
        :param message: message to log
        :param func_name: function name where we wrote log line
        :return:
        """
        if settings.LOG_DEBUG:
            self.log("debug", message, func_name)

    @classmethod
    def init_log(cls, func_name, logger=None, user="", client_id="", service_name=""):
        """
        :param func_name: function name where we wrote log line
        :param logger: logger object or logger name.
        :param user: username to log
        :param client_id: client_id to identify who call api
        :param service_name: service name to identify what service logged
        :return:
        """
        if not logger:
            init_service_name = service_name if service_name else settings.SERVICE_NAME
            log_message = cls(func_name=func_name, user=user, service_name=init_service_name)
        elif isinstance(logger, cls):
            user = logger.user
            init_service_name = service_name if service_name else logger.service_name
            log_message = cls(func_name=func_name, logger=logger.pub_logger, user=user, client_id=logger.client_id,
                              trace_id=logger.trace_id, service_name=init_service_name)
        elif isinstance(logger, MixingLog):
            user = logger.default.user
            init_service_name = service_name if service_name else logger.default.service_name
            log_message = cls(func_name=func_name, logger=logger.default.pub_logger, user=user,
                              client_id=logger.client_id, trace_id=logger.default.trace_id,
                              service_name=init_service_name)
        else:
            init_service_name = service_name if service_name else settings.SERVICE_NAME
            log_message = cls(func_name=func_name, logger=logger, user=user, client_id=client_id,
                              service_name=init_service_name)
        return log_message


class MixingLog(object):
    def __init__(self, func_name="", user=None, init_span=True, _parent_logger=None, client_id="", service_name=None):
        self.func_name = func_name
        self.user = user
        self.default = None
        self.client_id = client_id
        self._parent_logger = _parent_logger
        self.span = None
        self.init_span = init_span
        self.service_name = service_name if service_name else settings.SERVICE_NAME
        self.init_log_base_settings()

    @property
    def trace_id(self):
        return self.default.trace_id if self.default else uuid.uuid1().hex

    def set_user_log(self, username):
        self.user = username
        if self.default:
            self.default.set_user_log(username)

    def init_log_base_settings(self):
        if self.init_span:
            if isinstance(self._parent_logger, (LogMessage, MixingLog)):
                self.user = self._parent_logger.user
                self.client_id = self._parent_logger.client_id
        self.default = LogMessage(logger="", func_name=self.func_name, client_id=self.client_id, user=self.user,
                                  service_name=self.service_name)
        self.span = self.default.span
        for i in settings.LOGGING["loggers"].keys():
            if i:
                setattr(self, i,
                        LogMessage(logger=i, func_name=self.func_name, user=self.user, client_id=self.client_id,
                                   service_name=self.service_name))

    def set_component(self, value):
        return self.default.set_component(value)

    def info(self, message, func_name=""):
        self.default.info(message, func_name)

    def error(self, message, func_name=""):
        self.default.error(message, func_name)

    def warning(self, message, func_name=""):
        self.default.warning(message, func_name)

    def log(self, lv, message, func_name=""):
        self.default.log(lv, message, func_name)

    def debug(self, message, func_name=""):
        self.default.debug(message, func_name)
