import sqlite3
from pathlib import Path


MIGRATIONS_DIR = Path( __file__ ).parent


def migration_files():
   return sorted( MIGRATIONS_DIR.glob( '*.sql' ) )


def ensure_migration_table( cursor ):
   cursor.execute( ''' CREATE TABLE IF NOT EXISTS SchemaMigration
                     (  MIGRATION_NAME   TEXT NOT NULL PRIMARY KEY ); ''' )


def applied_migrations( cursor ):
   ensure_migration_table( cursor )

   return {
      row[ 0 ]
      for row in cursor.execute(
         'SELECT MIGRATION_NAME FROM SchemaMigration;'
      ).fetchall()
   }


def run_migrations( db_path='animals.db' ):
   conn = sqlite3.connect( db_path )
   cursor = conn.cursor()

   try:
      applied = applied_migrations( cursor )

      for migration_file in migration_files():
         migration_name = migration_file.name

         if migration_name in applied:
            continue

         cursor.executescript( migration_file.read_text() )
         cursor.execute(
            'INSERT INTO SchemaMigration ( MIGRATION_NAME ) VALUES ( ? );',
            ( migration_name, ) )

      conn.commit()

   finally:
      conn.close()


if __name__ == '__main__':
   run_migrations()
