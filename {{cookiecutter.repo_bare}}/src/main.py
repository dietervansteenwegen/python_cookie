#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

from config.config import Config
from {{cookiecutter.module_name}} import {{cookiecutter.class_name}}
from log.log import add_rotating_file, setup_logger
{% if cookiecutter.add_gui -%}
import sys
from gui.gui import start_gui
import logging

def excepthook(exc_type, exc_value, exc_tb) -> None:
    log=logging.getLogger()
    tabbed_msg: list[str] =[
        i.replace('\n', '\t').replace(' ', '')
        for i in traceback.format_exception(exc_type, exc_value, exc_tb) 
        ]
    for msg in tabbed_msg:
        log.error(msg)
        print(msg)


def gui():
    sys.excepthook = excepthook
    start_gui()
{%- endif %}

def _setup_log():
    """Set up logging."""    
    log = setup_logger()
    add_rotating_file(log)
    return log


def main():
    conf = Config()
    conf.get_config()
    {% if cookiecutter.add_gui %}
    gui()
    {% else %}
    {{cookiecutter.class_name}}(conf)
    {% endif %}

log = _setup_log()
log.info('Starting {{cookiecutter.project_name}}')

if __name__ == '__main__':
    main()
