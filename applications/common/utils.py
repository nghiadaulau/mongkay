import logging


class IgnoreChangeDetectedFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        print(record.msg)
        return "%d change%s detected: %s" != record.msg
