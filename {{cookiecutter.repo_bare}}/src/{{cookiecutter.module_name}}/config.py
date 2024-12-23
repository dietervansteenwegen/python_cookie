#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99


__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'
import argparse
import logging
from pathlib import Path
from typing import Union

import tomli

log = logging.getLogger(__name__)
PROGRAM_DESCRIPTION: str = '{{cookiecutter.project_name}}'


def get_arguments() -> argparse.Namespace:
    parser = HelpfullArgumentParser(
        add_help=True,
        description=PROGRAM_DESCRIPTION,
    )
    """Parse  and evaluate the supplied arguments.

    Returns:
        argparse.Namespace: Namespace containing the parsed arguments
    """
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
    """ArgumentParser subclass with improved error feedback.

    Provides better error message to user.
    """    
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
        self.config = None

    def get_config(self) -> None:
        self.arguments = get_arguments()
        if hasattr(self.arguments, 'config_file') and self.arguments.config_file:
            self._read_config_file()

    def _read_config_file(self) -> None:
        try:
            with Path(self.arguments.config_file).open(mode='rb') as f:
                self.config: dict = tomli.load(f)

        except FileNotFoundError:
            err_msg = f'Config file {self.arguments.config_file} does not exist.'
            raise FileNotFoundError(err_msg) from None

    def __str__(self) -> str:
        """String representation of the Config class."""

        msg = (
            f'Config with arguments {self.arguments} and config {self.config} '
            f'from file [{self.arguments.config_file}]'
        )
        return msg