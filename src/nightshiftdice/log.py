import logging

from anansi import parse_tags


class LogFormatter(logging.Formatter):
    base_format = '[{level_color} bold][%(levelname)s][/bold] %(message)s[/]'
    colors = {
        logging.DEBUG: 'yellow',
        logging.INFO: 'cyan',
        logging.WARNING: 'magenta',
        logging.ERROR: 'red',
        logging.CRITICAL: 'white',
    }

    def __init__(self):
        super().__init__(fmt='[%(levelname)s] %(message)s', style='%')

    def format(self, record):
        old_format = self._style._fmt
        self._style._fmt = parse_tags(LogFormatter.base_format.format(level_color=LogFormatter.colors[record.levelno]))
        result = logging.Formatter.format(self, record)
        self._style._fmt = old_format
        return result
