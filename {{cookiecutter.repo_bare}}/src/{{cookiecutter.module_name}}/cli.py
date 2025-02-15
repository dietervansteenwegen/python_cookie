#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

from .config import Config
from .log import add_rotating_file, setup_logger
from .{{cookiecutter.module_name}} import {{cookiecutter.class_name}}


def _setup_log():
    """Set up logging."""
    log = setup_logger()
    add_rotating_file(log)
    return log


log = _setup_log()
log.info('Starting {{cookiecutter.project_name}}')


def run():
    """Main command line entry point."""
    conf = Config()
    conf.get_config()
    {% if cookiecutter.add_gui %}gui(conf){% else %}{{cookiecutter.class_name}}(conf){% endif %}
