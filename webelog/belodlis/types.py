from typing import TypeVar
from pathlib import Path

from dlisio.dlis import PhysicalFile

InputFile = TypeVar('InputFile', PhysicalFile, str, Path)
