import sqlite3

from .loaders import seed_static_data
from .schema import create_schema


def main( db_path='animals.db' ):
   conn = sqlite3.connect( db_path )
   cursor = conn.cursor()

   try:
      create_schema( cursor )
      seed_static_data( cursor )
      conn.commit()
   finally:
      conn.close()

   print( 'Database and Animal table created successfully.' )
