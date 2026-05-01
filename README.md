# README

## How to use this?

Use `cruft create https://www.github.com/dietervansteenwegen/python_cookie.git` to generate a template.


{{cookiecutter.module_name}}.py needs:

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)
