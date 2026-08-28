from __future__ import annotations

import sqlite3

from .migrations.migration_runner import MigrationRunner
from .schema_creator import SchemaCreator
from .static_data_seeder import StaticDataSeeder

SEED_MIGRATIONS_START = '011_runtime_schema_column_additions.sql'


class SeedRunner():
   @classmethod
   def apply_schema( cls, db_path: str = 'animals.db' ) -> None:
      conn = sqlite3.connect( db_path )
      cursor = conn.cursor()

      try:
         SchemaCreator.create( cursor )
         MigrationRunner.run_on_cursor( cursor, skip_before=SEED_MIGRATIONS_START )
         conn.commit()
      finally:
         conn.close()


   @classmethod
   def apply_seed_data( cls, db_path: str = 'animals.db' ) -> None:
      conn = sqlite3.connect( db_path )
      cursor = conn.cursor()

      try:
         StaticDataSeeder.seed( cursor )
         conn.commit()
      finally:
         conn.close()


   @classmethod
   def main( cls, db_path: str = 'animals.db' ) -> None:
      conn = sqlite3.connect( db_path )
      cursor = conn.cursor()

      try:
         SchemaCreator.create( cursor )
         MigrationRunner.run_on_cursor( cursor, skip_before=SEED_MIGRATIONS_START )
         StaticDataSeeder.seed( cursor )
         conn.commit()
      finally:
         conn.close()

      print( 'Database schema and seed data applied successfully.' )


if __name__ == '__main__':
   SeedRunner.main()
