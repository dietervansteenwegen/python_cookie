#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99
import contextlib
import shlex
import subprocess
from pathlib import Path

def run_command(cmd:str, **kwargs):
    global to_log
    # Use shlex to split the command string (which may contain quote signs) into a list of arguments
    rtn = subprocess.run(shlex.split(cmd), capture_output= True, text=True, **kwargs)
    if rtn.returncode != 0:
        to_log.append([cmd, rtn.returncode,rtn.stderr, rtn.stdout])

def rmdir(directory):
    directory = Path(directory)
    with contextlib.suppress(FileNotFoundError):
        for item in directory.iterdir():
            if item.is_dir():
                rmdir(item)
            else:
                item.unlink()
        directory.rmdir()

def rm(file):
    global to_log
    file = Path(file)
    if file.is_file():
        file.unlink()
    else:
        to_log.append(f'Could not remove file {file}!', -1, '', '')

print('\n--> Generated files in "./{{cookiecutter.project_name_short}}".')
to_log:list[str] = []

############################
# DOCS
############################
{% if not cookiecutter.add_documentation %}
print('--> Removing documentation directory...', end = '', flush = True)
rmdir('docs')
print(' Done!')
{% endif %}

############################
# ASSETS DIRECTORY
############################
{% if not cookiecutter.create_assets_dir %}
rmdir('assets')
{% endif %}

############################
# CONFIG FILE
############################
{% if not cookiecutter.use_config_file %}
rm('config.toml')
{% endif %}

############################
# .env FILE
############################
{% if not cookiecutter.create_env_template %}
rm('.env')
{% endif %}

############################
# GUI
############################
{% if not cookiecutter.add_gui %}
print('--> cleaning up GUI...', end = '', flush = True)
rm('src/{{cookiecutter.module_name}}/gui.py')
rmdir('src/{{cookiecutter.module_name}}/ui_sources')
rmdir('assets/gui_sources')
print(' Done!')
{% else %}rm('src/{{cookiecutter.module_name}}/cli.py')
{% endif %}

############################
# DATA DIRECTORY
############################
{% if not cookiecutter.add_data_dir %}
print('--> cleaning up data directory...', end = '', flush = True)
rmdir('src/{{cookiecutter.module_name}}/data')
rm('src/{{cookiecutter.module_name}}/resources.py')
print(' Done!')
{% endif %}



############################
# GIT
############################
print('--> Initializing GIT...', end = '', flush = True)
run_command('git init --quiet')
run_command('git remote add origin git_prive:dietervansteenwegen/{{cookiecutter.project_name_short}}.git')
run_command('git checkout -b develop --quiet')
run_command('git add *')
run_command('git reset -- todo.md')
run_command('git commit -m "initial commit"')
run_command('git tag -a v0.0.0 -m "initial commit"')
print(' Done!')

############################
# FINISH
############################
def print_formatted(msg)-> None:
    print(f'*{msg: ^97}*')

print('\n' + '*' * 99)
print_formatted('Finished creating project "{{cookiecutter.project_name}}" in directory '
      '"./{{cookiecutter.project_name_short}}"...')
if to_log:
    print_formatted('')
    print_formatted('Errors with the following commands:')

    with open('cookiecutter.log', 'x') as output:
        for log in to_log:
            output.write('*' * 99)
            err_msg = f'\nCommand [{log[0]}] returned\n [{log[1]}]. \nOutput on stderr:\n {log[3]}\n'
            err_msg = f'Output on stdout: {log[2]}\n'
            output.write(err_msg)
            output.write('*' * 99)
            print_formatted(f'"{log[0]}"')
    print_formatted('')
    print_formatted('Check output logs in  "{{cookiecutter.project_name_short}}/cookiecutter.log"')
    print_formatted('')
print_formatted('Run \'make install\' and activate .venv to start developing.')
print_formatted('Run \'uv tool install .\' to install system-wide.')
print_formatted('Create remote repository dietervansteenwegen/{{cookiecutter.project_name_short}}.git')
print('*' * 99)
