#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

import sys
{% if cookiecutter.add_gui %}from .gui.gui import start_gui
import logging
import traceback
{% else -%}
from .cli import run{%- endif %}

"""Main entry point for ``python -m {{cookiecutter.module_name}}``."""

{% if cookiecutter.add_gui -%}
def excepthook(exc_type, exc_value, exc_tb) -> None:
    log=logging.getLogger()
    tabbed_msg: list[str] =[
        i.replace('\n', '\t').replace(' ', '')
        for i in traceback.format_exception(exc_type, exc_value, exc_tb) 
        ]
    for msg in tabbed_msg:
        log.error(msg)
        print(msg)


def gui(conf):
    sys.excepthook = excepthook
    start_gui(conf)
{%- else -%}
try:
    sys.exit(run())
except KeyboardInterrupt:
    sys.exit(1)
{% endif -%}
