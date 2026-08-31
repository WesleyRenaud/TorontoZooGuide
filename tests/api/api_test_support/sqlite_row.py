from __future__ import annotations

from collections.abc import Mapping
import sqlite3

from api.types import Types


def make_row( values: Mapping[ str, object ] ) -> Types.Row:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   columns = ', '.join( f'? AS { key }' for key in values.keys() )
   row = conn.execute( f'SELECT { columns }', tuple( values.values() ) ).fetchone()
   conn.close()

   assert row is not None

   return row
