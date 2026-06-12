from __future__ import annotations

import sqlite3

from .loaders import seed_static_data
from .migrations.runner import run_migrations_on_cursor
from .schema import create_schema

SEED_MIGRATIONS_START = '011_runtime_schema_column_additions.sql'


def apply_schema( db_path: str = 'animals.db' ) -> None:
   conn = sqlite3.connect( db_path )
   cursor = conn.cursor()

   try:
      create_schema( cursor )
      run_migrations_on_cursor( cursor, skip_before=SEED_MIGRATIONS_START )
      conn.commit()
   finally:
      conn.close()


def apply_seed_data( db_path: str = 'animals.db' ) -> None:
   conn = sqlite3.connect( db_path )
   cursor = conn.cursor()

   try:
      seed_static_data( cursor )
      conn.commit()
   finally:
      conn.close()


def main( db_path: str = 'animals.db' ) -> None:
   conn = sqlite3.connect( db_path )
   cursor = conn.cursor()

   try:
      create_schema( cursor )
      run_migrations_on_cursor( cursor, skip_before=SEED_MIGRATIONS_START )
      seed_static_data( cursor )
      conn.commit()
   finally:
      conn.close()

   print( 'Database schema and seed data applied successfully.' )


if __name__ == '__main__':
   main()
