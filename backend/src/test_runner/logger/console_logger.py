from datetime import datetime

from logger.logger import ILogger


class ConsoleLogger(ILogger):
    def _get_template(self, severity):
        return "{time} {severity} ".format(time=datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S'),
                                           severity=severity)

    def info(self, message):
        print(self._get_template("[INF]") + message)

    def error(self, message, exception):
        print(self._get_template("[ERROR]") + message + "\n" + str(exception))
