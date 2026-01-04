---
applyTo: "**/*.py"
---
# General
- Don't guess. Ask for clarification if requirements are unclear. Check your own answers for faulty assumptions.
- Follow PEP 8 style guide for Python code.
- Follow specifications (for Ruff,...) as described in the pyproject.toml (if it exists).
- Fix linting issues after making changes/adding code.
- Ensure code is compatible with Python 3.8 and above.
- Use timezone aware datetime objects.
- Don't extend past 99 characters per line.
- Put imports on top and order according to ruff (stdlib, third party, local)
- For small scripts, use inline script metadata according to pep 723

## Documentation/docstrings/typing
- Ensure functions, methods and classes have descriptive names.
- Write clear and concise docstrings for each function.
- Add Google style typing in docstrings.
- Use Sphinx-style formatting for docstrings.
- Use `Union[X, Y]` instead of PEP 604 (X | Y) for compatibility with Python 3.8 and 3.9.
- For complex functions, provide usage examples in the docstrings.
- Check AND UPDATE docstrings and type hints when making changes.
- Follow PEP 484/585/604 for type hinting.
- Whenever making significant changes, update the changelog in `CHANGELOG.md` in the "not yet released" section. Be brief. Prefix with "<copilot>"