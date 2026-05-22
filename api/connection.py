import sqlite3


def open_connection( db_path='animals.db' ):
   conn = sqlite3.connect( db_path )
   conn.row_factory = sqlite3.Row
   return conn


def close_connection( conn ):
   if conn is None:
      return

   conn.close()
