from __future__ import annotations

from .tables import static_tables
from ..types import Cursor


class StaticDataSeeder():
   @classmethod
   def seed( cls, cursor: Cursor ) -> None:
      for table in static_tables:
         table.insert_rows( cursor )
