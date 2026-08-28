from __future__ import annotations

from pathlib import Path

from ..types import Types


SEED_SQL_DIR = Path( __file__ ).parent / 'sql'


class SeedSqlLoader():
   @classmethod
   def seed_sql_path( cls, filename: str ) -> Path:
      return SEED_SQL_DIR / filename


   @classmethod
   def execute_sql_file( cls, cursor: Types.Cursor, path: Path ) -> None:
      cursor.executescript( path.read_text( encoding='utf-8' ) )
