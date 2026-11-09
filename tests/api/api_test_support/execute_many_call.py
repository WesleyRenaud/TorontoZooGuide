from __future__ import annotations

from typing import Any
from typing import NamedTuple


class ExecuteManyCall( NamedTuple ):
   sql: str
   rows: list[ list[ Any ] ]
