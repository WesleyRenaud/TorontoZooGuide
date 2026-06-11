from __future__ import annotations

from pathlib import Path

from ..types import Cursor


SEED_SQL_DIR = Path( __file__ ).parent / 'sql'


def seed_sql_path( filename: str ) -> Path:
   return SEED_SQL_DIR / filename


def execute_sql_file( cursor: Cursor, path: Path ) -> None:
   cursor.executescript( path.read_text( encoding='utf-8' ) )
