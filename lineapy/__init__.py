import atexit

from lineapy.api.api import catalog, get, save, to_airflow
from lineapy.data.graph import Graph
from lineapy.data.types import SessionType, ValueType
from lineapy.editors.ipython import start, visualize
from lineapy.editors.ipython_cell_storage import cleanup_cells
from lineapy.execution.context import get_context
from lineapy.instrumentation.tracer import Tracer
from lineapy.utils.lineabuiltins import db, file_system

__all__ = [
    "Graph",
    "Tracer",
    "save",
    "get",
    "catalog",
    "to_airflow",
    "SessionType",
    "ValueType",
    "_is_executing",
    "visualize",
    "db",
    "file_system",
    "__version__",
]

__version__ = "0.0.1"

# Create an ipython extension that starts and stops tracing
# https://ipython.readthedocs.io/en/stable/config/extensions/index.html#writing-extensions
# Can be used like %load_ext lineapy


def load_ipython_extension(ipython):
    atexit.register(cleanup_cells)
    start(ipython=ipython)


def unload_ipython_extension(ipython):
    cleanup_cells()


def _is_executing() -> bool:
    try:
        get_context()
    except RuntimeError:
        return False
    return True
