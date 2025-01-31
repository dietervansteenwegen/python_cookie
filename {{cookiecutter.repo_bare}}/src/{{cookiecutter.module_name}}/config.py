#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99


__author__ = 'Dieter Vansteenwegen'
__project__ = '{{cookiecutter.project_name}}'
__project_link__ = '{{cookiecutter.project_link}}'
import argparse
import logging
{% if cookiecutter.use_config_file -%}import tomli
from pathlib import Path{%- endif %}
from typing import Union

PROGRAM_DESCRIPTION: str = '{{cookiecutter.project_name}}'

log = logging.getLogger(__name__)


def get_arguments() -> argparse.Namespace:
    """Parse  and evaluate the supplied arguments.

    Returns:
        argparse.Namespace: Namespace containing the parsed arguments
    """
    parser = HelpfullArgumentParser(
        add_help=True,
        description=PROGRAM_DESCRIPTION,
    )
    # parser.add_argument('arg', nargs='*', help='Positional argument')
    ## ADD REQUIRED ARG BELOW THIS GROUP. OPTIONAL ABOVE...
    {%if cookiecutter.use_config_file -%}
    required_args = parser.add_argument_group('Required arguments')
    required_args.add_argument(
        '-c',
        '--config_file',
        help='Location of the config file.',
        action='store',
        dest='config_file',
        required=True,
    ){% else %}
    #required_args = parser.add_argument_group('Required arguments')
    # required_args.add_argument(
    #     '--src_fn',
    #     help='Source CSV to process.',
    # )
    {%- endif %}
    return parser.parse_args()


class HelpfullArgumentParser(argparse.ArgumentParser):
    """ArgumentParser subclass with improved error feedback.

    Provides better error message to user.
    """

    def error(self, msg):
        print('-' * 80)
        print(f'ERROR: {msg}\n')
        print('-' * 80)
        self.print_help()

        import sys

        sys.exit(-1)


class Config:
    def __init__(self):
        """Parses arguments and optionally configuration file for the application."""
        self.arguments: Union[None | argparse.Namespace] = {}
        self.config = None

    def get_config(self) -> None:
        """Get configuration from arguments and optionally a configuration file.

        If a config file is provided as one of the arguments, it will be read and stored 
        in the config attribute.
        """        
        self.arguments = get_arguments()
        {% if cookiecutter.use_config_file -%}if hasattr(self.arguments, 'config_file') and self.arguments.config_file:
            self._read_config_file()

    def _read_config_file(self) -> None:
        """Read the configuration file and store it in the config attribute.

        Parses the config file from the self.arguments.config_file attribute.

        Raises:
            FileNotFoundError: If the given config file does not exist.
        """        
        try:
            with Path(self.arguments.config_file).open(mode='rb') as f:
                self.config: dict = tomli.load(f)

        except FileNotFoundError:
            err_msg = f'Config file {self.arguments.config_file} does not exist.'
            raise FileNotFoundError(err_msg) from None{%- endif %}

    def __str__(self) -> str:
        """String representation of the Config class."""
        return (f'Config with arguments {self.arguments} and config {self.config} '
            {% if cookiecutter.use_config_file %}f'from file [{self.arguments.config_file}]'{% endif %}
        )
