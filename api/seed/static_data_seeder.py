from __future__ import annotations

from .tables import static_tables
from ..types import Types


class StaticDataSeeder():
   @classmethod
   def seed( cls, cursor: Types.Cursor ) -> None:
      for table in static_tables:
         table.insert_rows( cursor )
