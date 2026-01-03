# Python cookiecutter template CHANGELOG

## Not yet released

- build: Replace dead with Vulture
- feat: Add templating for dotenv loading
- build: bump Ruff pre-commit from 9.8 to 11.8
- feat: Add copilot instructions
- feat: Add precommit (local) hooks. Move Ruff to local.
- feat: Add versionioningit and auto-versioning
- fix (pyproject.toml): Cleanup
- feat: Add pre-commit-update hook
- feat: Improve ArgumentParser user feedback
- feat: Add data directory (included in packaging)
- feat: Add WIN32 and X11 environments if using a GUI
- fix: add correct module name in docstring
- feat: Include initial commit and v0.0.0 tag
- fix: move dev dependencies to a dependency group
- fix: Move project URL's to correct place in pyproject.toml
  
## v0.2.0 (03/03/2025)

- docs: Add documentation for argparse
- feature: Don't stage `todo.md` for commit
- bug: Move imports to beginning of file
- bug: Correct wrong indentation of post-op feedback
- bug: Put docstring at start of function
- fix: Correct autoformat breaking Jinja parsing
- feature: put log files in user home directory
- fix: Correct transitive dependency and absolute import
- feature: Extend the `prep` make recipe (Add lockfile sync, deptry and dead)
- feature: Add python version 3.12 for UV
- feature: Add prep_for_tagging make recipe
- feature: Flatten directory structure for GUI version
- refactor: Code cleanup
- feature: Migrate from PyQt5 to PySide6
- feature: Streamline similarities between gui/cli
- docs: Improve cookiecutter prompts and todo info
- docs: Rename repo_bare to project_name_short
- fix: Remove bandit settings and add ui_sources to exclude
- fix: Add Sphinx to dev deps if generating documentation
- fix: Don't strip all spaces from exception hook
- feat: Exit on destroyed MainWindow

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
