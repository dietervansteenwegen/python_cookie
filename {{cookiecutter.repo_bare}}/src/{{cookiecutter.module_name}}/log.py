#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99


__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

import datetime as dt
import logging
import logging.handlers
from pathlib import Path
from typing import Union
{% if cookiecutter.add_gui -%}from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDesktopWidget, QDialog, QHBoxLayout,
                             QPlainTextEdit){%- endif %}


LOG_FMT = (
    '%(asctime)s|%(levelname)-8.8s|%(module)-15.15s|%(lineno)-0.4d|%(funcName)-20.20s|%(message)s|'
)
DATEFMT = '%d/%m/%Y %H:%M:%S'
LOGFILE = './logs/{{cookiecutter.module_name}}.log'
LOG_FILE_MAX_BYTES = 1000000
LOG_BACKUP_COUNT = 10
TZ_UTC = dt.timezone.utc
CONSOLE_LOG_LEVEL = logging.INFO


class MilliSecondsFormatter(logging.Formatter):
    """Formats timestamp of log messages, keeping first three digits of milliseconds.


    Args:
        logging (logging.Formatter): formatter to add timestamp formatter to.
    """

    def formatTime(self, record: logging.LogRecord, datefmt: Union[str, None] = None) -> str:  # noqa: N802
        """Formats timestamp of log messages, keeping first three digits of milliseconds.

        Args:
            record (logging.LogRecord): LogRecord to apply formatting to.
            datefmt (Union[str, None], optional): datefmt for formatter. Uses DATEFMT is None.
                                                    Defaults to None.

        Returns:
            str: formatted timestamp for LogRecord
        """
        ct = dt.datetime.fromtimestamp(record.created).astimezone(TZ_UTC)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime(DATEFMT)
            s = f'{t}.{int(record.msecs):03}'
        return s


def setup_logger() -> logging.Logger:
    """Setup logging.

    Returns logging.Logger object with  1 streamhandler (to stdout).
    This handler has a level of CONSOLE_LOG_LEVEL uses MilliSecondsFormatter(LOG_FMT).

    Returns:
        logging.Logger: configured logger object
    """
    logger = logging.getLogger()  # DON'T specifiy name in order to create root logger!
    logger.setLevel(logging.DEBUG)
    add_console_handler(logger)
    return logger


def add_console_handler(logger: logging.Logger) -> None:
    """Add consolehandler to logger.


    Args:
        logger (logging.Logger): Logger to add handler to.
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(CONSOLE_LOG_LEVEL)
    console_handler.setFormatter(MilliSecondsFormatter(LOG_FMT))
    logger.addHandler(console_handler)


def add_rotating_file(logger: logging.Logger) -> None:
    """Add rotating file handler to Logger instance.

    Logfile used: LOGFILE
    Maximum log size: LOGMAXBYTES.
    Logging level set to DEBUG.
    Format set to LOG_FMT.
    Creates directory for logfiles if non-existent.

    Args:
        logger (logging.Logger): Logger to add handler to.
    """
    base = Path(LOGFILE).parent
    if not base.is_dir():
        logger.debug(f'Logging directory {base} does not exist. Creating...')
        base.mkdir(parents=True, exist_ok=True)
        logger.debug(f'Created logging directory {base}')
    rot_fil_handler = logging.handlers.RotatingFileHandler(
        LOGFILE,
        maxBytes=LOG_FILE_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
    )
    rot_fil_handler.doRollover()
    rot_fil_handler.setLevel(logging.DEBUG)
    rot_fil_handler.setFormatter(MilliSecondsFormatter(LOG_FMT))
    logger.addHandler(rot_fil_handler)

{%- if cookiecutter.add_gui -%}
class QTLogHandler(logging.Handler):
    """Logging handler for the QT logging dialog box.

    Args:
        logging (_type_): _description_
    """

    def __init__(self, parent):
        super().__init__()
        self.setLevel(logging.DEBUG)
        self.widget = QPlainTextEdit()
        self.widget.setReadOnly(True)
        self.widget.resize(1000, 200)
        self.widget.setLineWrapMode(QPlainTextEdit.NoWrap)  # type: ignore
        self.widget.setUndoRedoEnabled(False)
        self.layout = QHBoxLayout(parent)
        self.layout.addWidget(self.widget)
        self.setFormatter(MilliSecondsFormatter(LOG_FMT))

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg.__str__())


class DialogLog(QDialog):
    """Dialog window for the logging Handler."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Logging')
        self.resize(1000, 200)
        font = QFont('Monospace')
        font.setStyleHint(QFont.TypeWriter)  # type: ignore
        self.setFont(font)
        self._move_bottom_left()

    def _move_bottom_left(self):
        """Move dialog box to bottom left of current monitor."""
        monitor = QDesktopWidget().screenGeometry()
        window = self.geometry()

        y = (monitor.height() - 40) - window.height()
        self.move(0, y)
        log_text_box = QTLogHandler(self)
        logging.getLogger().addHandler(log_text_box)
{%- endif %}
