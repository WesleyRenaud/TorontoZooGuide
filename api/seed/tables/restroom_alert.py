from __future__ import annotations

from ..sql_loader import execute_sql_file
from ..sql_loader import seed_sql_path
from ...types import Cursor


SQL_FILE = 'restroom_alert.sql'


def create_table( cursor: Cursor ) -> None:
   execute_sql_file( cursor, seed_sql_path( SQL_FILE ) )
