# Python cookiecutter template CHANGELOG

## 18/06/2024

- use toml for config file
- Automatically install pip in virtual environment. Also install everything from requirements.txt.

## 16/09/2024

- Use datetime.timezone.utc instead of relying on pytz for timezone information
- Add tomli package to pyproject.toml
- Added `generate-hashes = True` to pip section of uv tool settings.

## 08/10/2024

- feat: Add exception hook for GUI use
- chore: Change email adress to <github@vansteenwegen.org>
- build: Upgrade to Python 3.12.6

## TODO

- When migrating to Python >=3.9: use `zoneinfo` library for timezone information.
