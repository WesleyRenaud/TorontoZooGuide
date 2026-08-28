from __future__ import annotations

from .tables import runtime_tables
from .tables import static_tables
from ..types import Cursor


class SchemaCreator():
   @classmethod
   def create( cls, cursor: Cursor ) -> None:
      for table in static_tables:
         table.create_table( cursor )

      for table in runtime_tables:
         table.create_table( cursor )
