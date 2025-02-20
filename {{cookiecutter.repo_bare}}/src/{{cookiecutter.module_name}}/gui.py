#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

# from PySide6 import QtCore as qtc
# from PySide6 import QtGui as qtg
from PySide6 import QtWidgets as qtw

from .config import Config
from .log import DialogLog
from .ui_sources.mainwindow import Ui_MainWindow


class MainWindow(Ui_MainWindow, qtw.QMainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.dialog_log: DialogLog = DialogLog(self)
        self.dialog_log.show()


def start_gui(config: Config) -> None:
    app = qtw.QApplication([])
    ui = MainWindow(config)  # noqa: F841
    ui.show()
    _ = app.exec_()


def run(config: Config):
    """Main command line entry point."""
    start_gui(config)  # noqa: F821
