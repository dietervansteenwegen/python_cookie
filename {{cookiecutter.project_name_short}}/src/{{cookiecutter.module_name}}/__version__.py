"""Runtime package version exposed as `{{cookiecutter.module_name}}.__version__`."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

try:
    __version__ = _pkg_version(distribution_name='{{cookiecutter.module_name}}')
except PackageNotFoundError:
    # Allows source-tree imports before the package is installed.
    __version__ = '0.0.0+unknown'
