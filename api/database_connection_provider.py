from __future__ import annotations

from pathlib import Path
import sqlite3

from .seed.schema_creator import SchemaCreator
from .shared.enums.position import Position
from .types import Types


class DatabaseConnectionProvider():
   DEFAULT_PATH = 'animals.db'
   ITINERARY_FILENAME = 'itinerary.db'
   ITINERARY_SCHEMA = 'itinerary'


   @classmethod
   def open( cls, db_path: str = DEFAULT_PATH ) -> Types.Connection:
      conn = sqlite3.connect( db_path )
      conn.row_factory = sqlite3.Row
      cls.attach_itinerary( conn, db_path )

      return conn


   @classmethod
   def open_read_only( cls, db_path: str | Path ) -> Types.Connection:
      path = Path( db_path )
      return sqlite3.connect( f'{ path.resolve().as_uri() }?mode=ro', uri=True )


   @classmethod
   def close( cls, conn: Types.Connection | None ) -> None:
      if conn is None:
         return

      conn.close()


   @classmethod
   def itinerary_path_beside( cls, animals_path: str | Path ) -> Path:
      return Path( animals_path ).expanduser().resolve().parent / cls.ITINERARY_FILENAME


   @classmethod
   def ensure_itinerary_schema( cls, itinerary_path: Path ) -> None:
      itinerary_path.parent.mkdir( parents=True, exist_ok=True )
      conn = sqlite3.connect( itinerary_path )
      cursor = conn.cursor()

      try:
         SchemaCreator.create_user_itinerary( cursor )
         conn.commit()
      finally:
         cursor.close()
         conn.close()


   @classmethod
   def itinerary_is_attached( cls, conn: Types.Connection ) -> bool:
      for row in conn.execute( 'PRAGMA database_list;' ).fetchall():
         if row[ Position.SECOND ] == cls.ITINERARY_SCHEMA:
            return True

      return False


   @classmethod
   def attach_itinerary( cls, conn: Types.Connection, animals_path: str | Path ) -> None:
      if animals_path == ':memory:':
         return

      itinerary_path = cls.itinerary_path_beside( animals_path )
      cls.ensure_itinerary_schema( itinerary_path )

      if cls.itinerary_is_attached( conn ):
         return

      conn.execute(
         f'ATTACH DATABASE ? AS { cls.ITINERARY_SCHEMA }',
         ( str( itinerary_path ), ),
      )
