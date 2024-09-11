# flake8: noqa: E501
from typing import Any, Optional, Union
from pydantic import BaseModel, Field
from dataclasses import dataclass
from dlisio.dlis import Fileheader

MAIN_PARAMETERS = [
    'CN', 'WN', 'FN',
    'NATI', 'CONT', 'FL',
    'FL1', 'FL2', 'LONG',
    'LATI', 'DLAB', 'TLAB',
    'CSIZ', 'THNO', 'BS'
]


@dataclass
class PhysicalFileSummary:
    """
    Entity to hold the description lines and a master dict of
    a summary representation of the file.
    """
    lines_desc: list[str]
    file_summary_dict: list[dict]
