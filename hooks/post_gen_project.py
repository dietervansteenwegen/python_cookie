#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99
import contextlib
from pathlib import Path

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
    file = Path(file)
    if file.is_file():
        file.unlink()
    else:
        print(f'----> Could not remove file {file}!')

print('\n\n--> Generated files, beginning post_gen_cleanup...\n')
############################
# DOCS
############################
{% if cookiecutter.add_documentation %}
import subprocess
print('--> Generating API documentation...')
subprocess.check_call(["sphinx-apidoc", 
                       "--force", 
                       "--output-dir", "./docs/source",
                    #    "./src/{{cookiecutter.module_name}}"])
                       "./src"])
print('--> Done\n')
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
print('--> Beginning GUI cleanup...')
rmdir('src/gui')
rmdir('assets/gui_sources')
print('--> Done\n')
{% endif %}


############################
# GIT
############################
{% if cookiecutter.init_git %}
print('--> Initializing GIT and pre-commit...')
import subprocess
subprocess.check_call(["git", "init", "--quiet"])
subprocess.check_call(["git", "remote", "add", "origin", "git_prive:dietervansteenwegen/{{cookiecutter.repo_bare}}.git"])
subprocess.check_call(["git", "checkout",  "-b",  "develop", "--quiet"])
subprocess.check_call(["pre-commit", "autoupdate"], stdout = subprocess.DEVNULL)
subprocess.check_call(["pre-commit", "install"], stdout = subprocess.DEVNULL)
subprocess.check_call(["git", "add", "*"])
print('--> Done\n')
{% endif %}

############################
# VENV
############################
{% if cookiecutter.create_venv %}
print('--> Setting up virtual environment...')
import venv
import subprocess
subprocess.check_call(["python", "-m", "pip", "install", "--upgrade", "--quiet", "pip"])
venv.create('venv')
print('--> Done\n')
{% endif %}


############################
# FINISH
############################
print('*' * 80)
print('   Finished creating project "{{cookiecutter.project_name}}" in directory '
      '"./{{cookiecutter.repo_bare}}"...')
{% if cookiecutter.create_venv %}
print('\n   --> Created a virtual environment, remember to activate it! <--')
{% endif %}

print('*' * 80)