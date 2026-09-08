from __future__ import annotations

from api.shared.enums.position import Position
from api.types import Types


def column_names( cursor: Types.Cursor, table: str ) -> set[ str ]:
   return {
      row[ Position.SECOND ]
      for row in cursor.execute( f'PRAGMA table_info( { table } );' ).fetchall()
   }
