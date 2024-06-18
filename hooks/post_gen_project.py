#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99
import contextlib
import subprocess
from pathlib import Path

to_log:list[str] = []

def run_command(cmd:str):
    global to_log
    rtn = subprocess.run(cmd.split(' '), capture_output= True, text=True,)
    if rtn.returncode != 0:
        # to_log.append(f'{cmd} returned {rtn.returncode}: \n {rtn.stderr}\n{rtn.stdout}')
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
        to_log.append[f'Could not remove file {file}!', -1, '', '']

print('\n--> Generated files in "./{{cookiecutter.repo_bare}}", beginning cleanup...')

############################
# DOCS
############################
{% if cookiecutter.add_documentation %}
print('--> Generating API documentation...', end = '')
subprocess.check_call(["sphinx-apidoc", 
                       "--force", 
                       "--output-dir", "./docs/source",
                    #    "./src/{{cookiecutter.module_name}}"])
                       "./src"])
print(' Done\n')
{% else %}
rmdir('docs')
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
{% if not cookiecutter.require_config_file %}
rm('config.ini')
{% endif %}

############################
# GUI
############################
{% if not cookiecutter.add_gui %}
print('--> Beginning GUI cleanup...', end = '')
rmdir('src/gui')
rmdir('assets/gui_sources')
print(' Done')
{% endif %}

############################
# GIT
############################
{% if cookiecutter.init_git %}
print('--> Initializing GIT and pre-commit...')
run_command('git init --quiet')
run_command('git remote add origin git_prive:dietervansteenwegen/{{cookiecutter.repo_bare}}.git')
run_command('git checkout -b develop --quiet')
# subprocess.check_call(["pre-commit", "autoupdate"], stdout = subprocess.DEVNULL)
run_command('pre-commit autoupdate')
run_command('pre-commit install')
# subprocess.check_call(["pre-commit", "install"], 
#                       stdout = subprocess.DEVNULL, 
#                       stderr = subprocess.DEVNULL,
#                       )
run_command('git add *')
run_command('pre-commit run --all-files')

print('--> Done')
{% endif %}

############################
# VENV
############################
{% if cookiecutter.create_venv %}
print('--> Setting up virtual environment...', end='')
import venv
run_command('python -m pip install --upgrade --quiet pip')
venv.create('venv')
print('Done')
{% endif %}

############################
# FINISH
############################
def print_formatted(msg)-> None:
    print(f'*{msg: ^78}*')

print('\n' + '*' * 80)
print_formatted('Finished creating project "{{cookiecutter.project_name}}" in directory '
      '"./{{cookiecutter.repo_bare}}"...')
if to_log:
    print_formatted('')
    print_formatted('Errors with the following commands:')
    with open('cookiecutter.log', 'x') as output:
        for log in to_log:
            print_formatted(log[0])
            output.write('*' * 80)
            err_msg = f'Command {log[0]} returned {log[1]}. Output: {log[2]}\n{log[3]}'
            output.write(err_msg)
            output.write('*' * 80)
    print_formatted('Check output logs in  "./cookiecutter.log"')
    print_formatted('')
{% if cookiecutter.create_venv %}
print_formatted('--> Created a virtual environment, remember to activate it and run python '
                '-m ensurepip! <--')
{% endif %}
print('*' * 80)
