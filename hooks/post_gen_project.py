#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99
import contextlib
import subprocess
from pathlib import Path
import os
import os.path
import pathlib
import sys
import venv
from subprocess import PIPE, Popen
from threading import Thread
from urllib.parse import urlparse
from urllib.request import urlretrieve

# Based on example from https://docs.python.org/3/library/venv.html#venv.EnvBuilder.setup_scripts


class EnvBuilderWithRequirements(venv.EnvBuilder):
    """
    This builder installs setuptools and pip so that you can pip or
    easy_install other packages into the created virtual environment.

    :param nodist: If true, setuptools and pip are not installed into the
                   created virtual environment.
    :param nopip: If true, pip is not installed into the created
                  virtual environment.
    :param progress: If setuptools or pip are installed, the progress of the
                     installation can be monitored by passing a progress
                     callable. If specified, it is called with two
                     arguments: a string indicating some progress, and a
                     context indicating where the string is coming from.
                     The context argument can have one of three values:
                     'main', indicating that it is called from virtualize()
                     itself, and 'stdout' and 'stderr', which are obtained
                     by reading lines from the output streams of a subprocess
                     which is used to install the app.

                     If a callable is not specified, default progress
                     information is output to sys.stderr.
    """

    def __init__(self, *args, **kwargs):
        self.nodist = kwargs.pop("nodist", False)
        self.nopip = kwargs.pop("nopip", False)
        self.progress = kwargs.pop("progress", None)
        self.verbose = kwargs.pop("verbose", False)
        self.install_from_requirements = kwargs.pop("install_requirements", True)
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        Set up any packages which need to be pre-installed into the
        virtual environment being created.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        os.environ["VIRTUAL_ENV"] = context.env_dir
        if not self.nodist:
            self.install_setuptools(context)
        # Can't install pip without setuptools
        if not self.nopip and not self.nodist:
            self.install_pip(context)
        if self.install_from_requirements:
            self.install_requirements(context)

    def install_requirements(self, context):
        binpath = context.bin_path
        if sys.platform.startswith("linux"):
            executable = "pip"
        else:
            executable = "pip.exe"
        pip_path = pathlib.Path(binpath, executable)
        requirement_fn = pathlib.Path(pathlib.Path.cwd(), "requirements.txt")  
        # p = Popen([pip_path, "install", "-r", requirement_fn], stdout=None, stderr=None,)
        print(f'Running pip {pip_path} to install from {requirement_fn}')
        run_command(f'{pip_path} install -r {requirement_fn}')
        #TODO: use 
        # t1 = Thread(target=self.reader, args=(p.stdout, "stdout"))
        # t1.start()
        # t2 = Thread(target=self.reader, args=(p.stderr, "stderr"))
        # t2.start()
        # p.wait()
        # t1.join()
        # t2.join()

    def reader(self, stream, context):
        """
        Read lines from a subprocess' output stream and either pass to a progress
        callable (if specified) or write progress information to sys.stderr.
        """
        progress = self.progress
        while True:
            s = stream.readline()
            if not s:
                break
            if progress is not None:
                progress(s, context)
            else:
                if not self.verbose:
                    sys.stderr.write(".")
                else:
                    sys.stderr.write(s.decode("utf-8"))
                sys.stderr.flush()
        stream.close()

    def install_script(self, context, name, url):
        _, _, path, _, _, _ = urlparse(url)
        fn = os.path.split(path)[-1]
        binpath = context.bin_path
        distpath = os.path.join(binpath, fn)
        # Download script into the virtual environment's binaries folder
        urlretrieve(url, distpath)
        # progress = self.progress
        # if self.verbose:
        #     term = "\n"
        # else:
        #     term = ""
        # args = [context.env_exe, fn]
        run_command(f'{context.env_exe} {fn}', cwd = binpath)
        # p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=binpath)
        # t1 = Thread(target=self.reader, args=(p.stdout, "stdout"))
        # t1.start()
        # t2 = Thread(target=self.reader, args=(p.stderr, "stderr"))
        # t2.start()
        # p.wait()
        # t1.join()
        # t2.join()
        # if progress is not None:
        #     progress("done.", "main")
        # else:
        #     sys.stderr.write("done.\n")
        # Clean up - no longer needed
        os.unlink(distpath)

    def install_setuptools(self, context):
        """
        Install setuptools in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = "https://bootstrap.pypa.io/ez_setup.py"
        self.install_script(context, "setuptools", url)
        # clear up the setuptools archive which gets downloaded
        pred = lambda o: o.startswith("setuptools-") and o.endswith(".tar.gz")
        files = filter(pred, os.listdir(context.bin_path))
        for f in files:
            f = os.path.join(context.bin_path, f)
            os.unlink(f)

    def install_pip(self, context):
        """
        Install pip in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = "https://bootstrap.pypa.io/get-pip.py"
        self.install_script(context, "pip", url)

def run_command(cmd:str, **kwargs):
    global to_log
    rtn = subprocess.run(cmd.split(' '), capture_output= True, text=True, **kwargs)
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
        to_log.append[f'Could not remove file {file}!', -1, '', '']

print('\n--> Generated files in "./{{cookiecutter.repo_bare}}".')
to_log:list[str] = []

############################
# DOCS
############################
{% if cookiecutter.add_documentation %}
print('--> Generating API documentation...', end = '', flush = True)
subprocess.check_call(["sphinx-apidoc", 
                       "--force", 
                       "--output-dir", "./docs/source",
                    #    "./src/{{cookiecutter.module_name}}"])
                       "./src"])
print(' Done')
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
rm('config.toml')
{% endif %}

############################
# GUI
############################
{% if not cookiecutter.add_gui %}
print('--> cleaning up GUI...', end = '', flush = True)
rmdir('src/{{cookiecutter.module_name}}/gui')
rmdir('assets/gui_sources')
print(' Done!')
{% endif %}

############################
# GIT
############################
{% if cookiecutter.init_git %}
print('--> Initializing GIT and pre-commit...', end = '', flush = True)
run_command('git init --quiet')
run_command('git remote add origin git_prive:dietervansteenwegen/{{cookiecutter.repo_bare}}.git')
run_command('git checkout -b develop --quiet')
# subprocess.check_call(["pre-commit", "autoupdate"], stdout = subprocess.DEVNULL)
run_command('pre-commit autoupdate')
run_command('pre-commit install')
run_command('git add *')
run_command('pre-commit run --all-files')
print(' Done!')
{% endif %}

############################
# VENV
############################
{% if cookiecutter.create_venv %}
print('--> Setting up virtual environment...', end='', flush = True)
run_command('python -m pip install --upgrade --quiet pip')
v = EnvBuilderWithRequirements(with_pip=True, upgrade_deps = True)
v.create('venv')
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
            output.write('*' * 80)
            err_msg = f'\nCommand [{log[0]}] returned\n [{log[1]}]. \nOutput on stderr: {log[3]}\n'
            err_msg = f'Output on stdout: {log[2]}\n'
            output.write(err_msg)
            output.write('*' * 80)
            print_formatted(f'"{log[0]}"')
    print_formatted('')
    print_formatted('Check output logs in  "{{cookiecutter.repo_bare}}/cookiecutter.log"')
    print_formatted('')
{% if cookiecutter.create_venv %}
print_formatted('--> Created a virtual environment, remember to activate it! <--')
{% endif %}
print('*' * 80)
