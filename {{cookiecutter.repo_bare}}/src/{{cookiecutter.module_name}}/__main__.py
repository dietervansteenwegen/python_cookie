#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

from {{cookiecutter.module_name}}.config import Config
from {{cookiecutter.module_name}}.{{cookiecutter.module_name}} import {{cookiecutter.class_name}}
from {{cookiecutter.module_name}}.log import add_rotating_file, setup_logger
import sys
{% if cookiecutter.add_gui -%}from gui.gui import start_gui
import logging
import traceback

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
    start_gui(conf){%- endif %}

def _setup_log():
    """Set up logging."""    
    log = setup_logger()
    add_rotating_file(log)
    return log

log = _setup_log()
log.info('Starting {{cookiecutter.project_name}}')

def run():
    conf = Config()
    conf.get_config()
    {% if cookiecutter.add_gui %}
    gui(conf){% else %}{{cookiecutter.class_name}}(conf)
    {% endif %}


if __name__ == '__main__':
    sys.exit(run())
