#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99


__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'
import argparse
import logging
from configparser import ConfigParser
from pathlib import Path
from typing import Union

log = logging.getLogger(__name__)
PROGRAM_DESCRIPTION: str = '{{cookiecutter.project_name}}'


def get_arguments() -> argparse.Namespace:
    parser = HelpfullArgumentParser(
        add_help=True,
        description=PROGRAM_DESCRIPTION,
    )

    {%if- cookiecutter.require_config_file -%}

    ## ADD REQUIRED ARG BELOW THIS GROUP. OPTIONAL ABOVE...
    required_args = parser.add_argument_group('Required arguments')
    required_args.add_argument(
        '-c',
        '--config_file',
        help='Location of the config file.',
        action='store',
        dest='config_file',
        required=True,
    )

    {%- else -%}

    parser.add_argument(
        '-c',
        '--config_file',
        help='Location of the config file functionality.',
        action='store',
        dest='config_file',
        required=False,
    )
    ## ADD REQUIRED ARG BELOW THIS GROUP. OPTIONAL ABOVE...
    # required_args = parser.add_argument_group('Required arguments')
    # required_args.add_argument(

    {% endif %}

    return parser.parse_args()

class HelpfullArgumentParser(argparse.ArgumentParser):
    def error(self, msg):
        print('-'*80)
        print(f'\nERROR: {msg}\n\n')
        print('-'*80)
        self.print_help()

        {%if- cookiecutter.require_config_file -%}
        import sys
        sys.exit(-1)
        {% endif %}


class Config:
    def __init__(self):
        self.arguments:Union[None|argparse.Namespace] = {}
        self.config_fn:Union[None|Path] = None
        self.config = None

    def get_config(self):
        self.arguments = get_arguments()
        if hasattr(self.arguments, 'config_file') and self.arguments.config_file:
            self._get_config_file()

    def _get_config_file(self):
        if Path(self.arguments.config_file).is_file():
            self.config_fn = Path(self.arguments.config_file)
            log.info(f'Reading config file {self.config_fn}')
            self.config = ConfigParser()
            self.config.read(self.config_fn)
        else:
            err_msg = f'Config file {self.arguments.config_file} is not a file.'
            log.warning(err_msg)
            self.config = None

    def __str__(self):
        _sections: list[str] = self.config.sections()
        _sections.append('DEFAULT')
        all_conf = []
        for section in _sections:
            for key, value in self.config.items(section):
                all_conf.append([section, key, value])

        msg = (
            f'Config with arguments {self.arguments} and config {all_conf} '
            f'from file [{self.config_fn}]'
        )
        return msg