from __future__ import annotations

from typing import Any
from typing import NamedTuple


class CoordinatorCall( NamedTuple ):
   name: str
   arguments: dict[ str, Any ]
