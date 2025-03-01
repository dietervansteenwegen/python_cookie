#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'

from .config import Config
from .{{cookiecutter.module_name}} import {{cookiecutter.class_name}}



def run(config: Config):
    """Main command line entry point."""
    {{cookiecutter.class_name}}(config)
