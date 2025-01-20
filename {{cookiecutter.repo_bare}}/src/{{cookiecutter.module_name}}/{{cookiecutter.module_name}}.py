#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

import logging

from {{cookiecutter.module_name}}.config import Config

log = logging.getLogger(__name__)


class {{cookiecutter.class_name}}:
    def __init__(self, config: Config):
        log.info(f'{{cookiecutter.class_name}} initialized. Config: {config}')
