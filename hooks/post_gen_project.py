#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99
from pathlib import Path

def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()

{% if cookiecutter.add_documentation %}
import subprocess
print('--> Generating API documentation')
subprocess.check_call(["sphinx-apidoc", 
                       "--force", 
                       "--output-dir", "./docs/source",
                    #    "./src/{{cookiecutter.module_name}}"])
                       "./src"])
print('--> Done\n')
{% else %}
rmdir('docs')
{% endif %}

{% if not cookiecutter.create_assets_dir %}
rmdir('assets')
{% endif %}




{% if cookiecutter.init_git %}
print('--> Initializing GIT and pre-commit...')
import subprocess
subprocess.check_call(["git", "init"])
subprocess.check_call(["git", "remote", "add", "origin", "git_prive:dietervansteenwegen/{{cookiecutter.repo_bare}}.git"])
subprocess.check_call(["git", "checkout",  "-b",  "develop"])
subprocess.check_call(["pre-commit", "autoupdate"])
subprocess.check_call(["pre-commit", "install"])
print('--> Done\n')
{% endif %}

{% if cookiecutter.create_venv %}
import venv
import subprocess
subprocess.check_call(["python", "-m", "pip", "install", "--upgrade", "--quiet", "pip"])
venv.create('venv')
print('\n--> Created a virtual environment, remember to activate it!\n')
{% endif %}

print('*' * 80)
print('Finished creating project "{{cookiecutter.project_name}}" in directory '
      '"./{{cookiecutter.repo_bare}}" !')
{% if cookiecutter.create_venv %}
print('\n--> Created a virtual environment, remember to activate it! <--')
{% endif %}

print('*' * 80)