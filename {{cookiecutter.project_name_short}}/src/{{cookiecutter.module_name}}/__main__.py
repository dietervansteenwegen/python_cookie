#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

import sys
from .config import Config
{% if cookiecutter.add_gui %}from .gui import run
import logging
import traceback
{% else -%}
from .cli import run{%- endif %}
from .log import add_rotating_file, setup_logger

"""Main entry point for `python -m {{cookiecutter.module_name}}`."""

def _setup_log():
    """Set up logging."""
    log = setup_logger()
    add_rotating_file(log)
    return log

{% if cookiecutter.add_gui -%}
def excepthook(exc_type, exc_value, exc_tb) -> None:
    log = logging.getLogger(__name__)
    tabbed_msg: list[str] = [
        i.replace('\n', '\t').replace('  ', ' ')
        for i in traceback.format_exception(exc_type, exc_value, exc_tb)
        ]
    for msg in tabbed_msg:
        log.error(msg)
        print(msg)


sys.excepthook = excepthook
{% endif %}
log = _setup_log()
try:
    config = Config()
    config.get_config()
    log.debug(f'Starting {{cookiecutter.project_name}} with config {config}')
    sys.exit(run(config))
except KeyboardInterrupt:
    sys.exit(1)
