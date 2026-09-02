from __future__ import annotations

from api.types import Types


def column_names( cursor: Types.Cursor, table: str ) -> set[ str ]:
   return {
      row[ 1 ]
      for row in cursor.execute( f'PRAGMA table_info( { table } );' ).fetchall()
   }
