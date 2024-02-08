from unidock_tools.utils import init_logging

init_logging()

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("binary4fun")
except PackageNotFoundError:
    __version__ = "unknown"