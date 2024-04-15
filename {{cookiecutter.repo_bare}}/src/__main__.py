#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

from config.config import Config
from log.log import add_rotating_file, setup_logger
from {{cookiecutter.module_name}} import {{cookiecutter.class_name}}
{% if cookiecutter.add_gui %}
from gui.gui import start_gui
{% endif %}

log = setup_logger()
add_rotating_file(log)

{% if cookiecutter.add_gui %}
def gui():
    start_gui()
{% endif %}


def main():
    conf = Config()
    conf.get_config()
    {% if cookiecutter.add_gui %}
    gui()
    {% else %}
    {{cookiecutter.class_name}}(conf)
    {% endif %}


if __name__ == '__main__':
    main()
