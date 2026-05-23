from __future__ import annotations

from .tables import static_tables
from ..types import Cursor


def seed_static_data( cursor: Cursor ) -> None:
   for table in static_tables:
      table.insert_rows( cursor )
