from __future__ import annotations

from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


SQL_FILE = 'wild_encounter_schedule.sql'


class WildEncounterScheduleSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )
