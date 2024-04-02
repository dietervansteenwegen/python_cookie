#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

import sys
import traceback
from typing import List

from log.log import add_rotating_file, setup_logger
from PyQt5 import QtWidgets as qtw
from ui_sources.mainwindow import Ui_MainWindow

log = setup_logger()
add_rotating_file(log)


class MainWindow(Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        log.debug('Starting MainWindow')
        self.setupUi(self)


def excepthook(exc_type, exc_value, exc_tb) -> None:
    tabbed_msg: List[str] = [
        i.replace('\n', '\t').replace('  ', '')
        for i in traceback.format_exception(exc_type, exc_value, exc_tb)
    ]
    log.error('|'.join(tabbed_msg), exc_info=True, stack_info=True)
    qtw.QApplication.quit()


def start_gui() -> None:
    log = setup_logger()
    add_rotating_file(log)
    log.debug('Root logger initialized.')
    sys.excepthook = excepthook
    app = qtw.QApplication([])
    window: MainWindow = MainWindow()
    window.show()
    rtn = app.exec_()
    log.info(f'Exited: {rtn if rtn != 0 else "clean"}')
