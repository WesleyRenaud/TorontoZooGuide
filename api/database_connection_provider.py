from pathlib import Path
import sqlite3

from .types import Types


class DatabaseConnectionProvider():
   @classmethod
   def open( cls, db_path: str = 'animals.db' ) -> Types.Connection:
      conn = sqlite3.connect( db_path )
      conn.row_factory = sqlite3.Row
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
