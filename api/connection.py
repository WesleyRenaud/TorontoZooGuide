import sqlite3

from .types import Connection


def open_connection( db_path: str = 'animals.db' ) -> Connection:
   conn = sqlite3.connect( db_path )
   conn.row_factory = sqlite3.Row
   return conn


def close_connection( conn: Connection | None ) -> None:
   if conn is None:
      return

   conn.close()
