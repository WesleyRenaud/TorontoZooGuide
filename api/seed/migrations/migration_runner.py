from __future__ import annotations

from pathlib import Path
import re
import sqlite3

from ...types import Types


MIGRATIONS_DIR = Path( __file__ ).parent
ALTER_ADD_COLUMN_PATTERN = re.compile(
   r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+COLUMN\s+(\w+)',
   re.IGNORECASE,
)


class MigrationRunner():
   @classmethod
   def migration_files( cls ) -> list[ Path ]:
      return sorted( MIGRATIONS_DIR.glob( '*.sql' ) )


   @classmethod
   def ensure_migration_table( cls, cursor: Types.Cursor ) -> None:
      cursor.execute( ''' CREATE TABLE IF NOT EXISTS SchemaMigration
                        (  MIGRATION_NAME   TEXT NOT NULL PRIMARY KEY ); ''' )


   @classmethod
   def applied_migrations( cls, cursor: Types.Cursor ) -> set[ str ]:
      cls.ensure_migration_table( cursor )

      return {
         row[ 0 ]
         for row in cursor.execute(
            'SELECT MIGRATION_NAME FROM SchemaMigration;'
         ).fetchall()
      }


   @classmethod
   def _table_columns( cls, cursor: Types.Cursor, table: str ) -> set[ str ]:
      return {
         row[ 1 ]
         for row in cursor.execute( f'PRAGMA table_info( { table } );' ).fetchall()
      }


   @classmethod
   def _split_sql_statements( cls, script: str ) -> list[ str ]:
      return [
         statement.strip()
         for statement in script.split( ';' )
         if statement.strip()
      ]


   @classmethod
   def _execute_migration_statement( cls, cursor: Types.Cursor, statement: str ) -> None:
      match = ALTER_ADD_COLUMN_PATTERN.search( statement )

      if match is not None:
         table_name = match.group( 1 )
         column_name = match.group( 2 )
         existing_columns = cls._table_columns( cursor, table_name )

         if not existing_columns or column_name in existing_columns:
            return

      try:
         cursor.execute( statement )
      except sqlite3.OperationalError as error:
         message = str( error ).lower()

         if 'duplicate column name' in message or 'no such table' in message or 'no such column' in message:
            return

         raise


   @classmethod
   def _record_migration( cls, cursor: Types.Cursor, migration_name: str ) -> None:
      cursor.execute(
         'INSERT INTO SchemaMigration ( MIGRATION_NAME ) VALUES ( ? );',
         ( migration_name, ),
      )


   @classmethod
   def run_on_cursor(
         cls,
         cursor: Types.Cursor,
         *,
         skip_before: str | None = None,
      ) -> None:
      applied = cls.applied_migrations( cursor )

      for migration_file in cls.migration_files():
         migration_name = migration_file.name

         if migration_name in applied:
            continue

         if skip_before is not None and migration_name < skip_before:
            cls._record_migration( cursor, migration_name )
            continue

         for statement in cls._split_sql_statements( migration_file.read_text() ):
            cls._execute_migration_statement( cursor, statement )

         cls._record_migration( cursor, migration_name )


   @classmethod
   def run( cls, db_path: str = 'animals.db' ) -> None:
      conn = sqlite3.connect( db_path )
      cursor = conn.cursor()

      try:
         cls.run_on_cursor( cursor )
         conn.commit()
      finally:
         conn.close()


if __name__ == '__main__':
   MigrationRunner.run()
