import logging


class LogFormatter(logging.Formatter):
    base_format = '[{level_color} bold][%(levelname)s][/bold] %(message)s[/]'
    colors = {
        logging.DEBUG: 'yellow',
        logging.INFO: 'cyan',
        logging.WARNING: 'orange',
        logging.ERROR: 'red',
        logging.CRITICAL: 'magenta',
    }
