import sqlite3

from .types import Types


class DatabaseConnectionProvider():
   @classmethod
   def open( cls, db_path: str = 'animals.db' ) -> Types.Connection:
      conn = sqlite3.connect( db_path )
      conn.row_factory = sqlite3.Row
      return conn


   @classmethod
   def close( cls, conn: Types.Connection | None ) -> None:
      if conn is None:
         return

      conn.close()
