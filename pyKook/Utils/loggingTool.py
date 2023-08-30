import inspect
from .singleton import singleton


@singleton
class logger:
    def __init__(self, log_level: int = 0):
        self._log_level = log_level

    def _get_caller_label(self):
        # caller -> logger.debug -> logger._log -> logger._get_caller_label
        prev_frame = inspect.currentframe().f_back.f_back.f_back
        (filename, line_number, function_name, lines, index) = inspect.getframeinfo(
            prev_frame
        )
        return "\033[1;37m{}\033[0m:\033[1;37m{}\033[0m::\033[1;37m{}\033[0m ".format(
            filename.split("/")[-1], line_number, function_name
        )

    def _log(self, level, msg):
        prefix = ""
        match level:
            case 0:
                # gray [DEBUG]
                prefix += "\033[1;30m[DEBUG]\033[0m"
            case 1:
                # white [INFO]
                prefix += "\033[1;37m[INFO]\033[0m"
            case 2:
                # yellow [WARNING]
                prefix += "\033[1;33m[WARNING]\033[0m"
            case 3:
                # red [ERROR]
                prefix += "\033[1;31m[ERROR]\033[0m"
            case 4:
                # green [SUCCESS]
                prefix += "\033[1;32m[SUCCESS]\033[0m"
            case _:
                # white [INFO]
                prefix += "\033[1;37m[INFO]\033[0m"
        prefix += " " + self._get_caller_label()
        if level >= self._log_level:
            print(prefix, msg)

    def debug(self, msg):
        self._log(0, msg)

    def info(self, msg):
        self._log(1, msg)

    def warning(self, msg):
        self._log(2, msg)

    def error(self, msg):
        self._log(3, msg)

    def success(self, msg):
        self._log(4, msg)


logging = logger()
