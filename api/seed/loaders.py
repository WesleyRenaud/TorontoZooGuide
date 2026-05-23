from __future__ import annotations

from ..types import Cursor
from .tables import static_tables


def seed_static_data( cursor: Cursor ) -> None:
   for table in static_tables:
      table.insert_rows( cursor )
