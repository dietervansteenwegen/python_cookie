# Python cookiecutter template CHANGELOG

## Not released yet

- feature: Don't stage `todo.md` for commit

## v0.1.0 (20/01/2025)

- feat: Migrate from `PIP` and `VENV` to  `UV`
- feat: Major cleanup

## 08/10/2024

- feat: Add exception hook for GUI use
- chore: Change email adress to <github@vansteenwegen.org>
- build: Upgrade to Python 3.12.6

## 16/09/2024

- Use datetime.timezone.utc instead of relying on pytz for timezone information
- Add tomli package to pyproject.toml
- Added `generate-hashes = True` to pip section of uv tool settings.

## 18/06/2024

- use toml for config file
- Automatically install pip in virtual environment. Also install everything from requirements.txt.
