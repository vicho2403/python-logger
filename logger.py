from datetime import datetime
from sys import exc_info


class Logger:
    LEVELS = {
        'debug': 4,
        'info': 3,
        'warning': 2,
        'error': 1,
    }

    def __init__(self, level='debug'):
        self.level = self.LEVELS.get(level)

    def _must_hide(self, level):
        return self.LEVELS.get(level) > self.level

    @staticmethod
    def __set_text(color, text):
        time_now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f] ")
        return ''.join([color, time_now, text, '\033[0m'])

    @staticmethod
    def __print_text(color, header, text, *args, **kwargs):
        if args:
            text = ' '.join([str(text)] + list(map(lambda x: str(x), args)))

        if kwargs.get('break_line', False):
            print('')

        print(Logger.__set_text(color, header + ': ' + str(text)))

    def debug(self, text, *args, **kwargs):
        if self._must_hide('debug'):
            return
        Logger.__print_text('\033[96m', 'DEBUG', text, *args, **kwargs)

    def info(self, text, *args, **kwargs):
        if self._must_hide('info'):
            return
        Logger.__print_text('\033[39m', 'INFO', text, *args, **kwargs)

    def warning(self, text, *args, **kwargs):
        if self._must_hide('warning'):
            return
        Logger.__print_text('\033[93m', 'WARNING', text, *args, **kwargs)

    @staticmethod
    def success(text, *args, **kwargs):
        if args:
            text = ' '.join([text] + list(map(lambda x: str(x), args)))
        Logger.__print_text('\033[1m' + '\033[92m', 'SUCCESS', text + '\033[0m', **kwargs)

    def error(self, text, *args, **kwargs):
        if self._must_hide('error'):
            return
        try:
            text = ' '.join(['Error on line {} -'.format(exc_info()[-1].tb_lineno), str(text)])
        except AttributeError:
            pass
        Logger.__print_text('\033[91m', 'ERROR', text, *args, **kwargs)
