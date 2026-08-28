from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


RECORD_FIELDS = [
   'name',
   'location',
   'x_coord',
   'y_coord',
   'maximum_duration',
]

DB_COLUMNS = [
   'NAME',
   'LOCATION',
   'X_COORD',
   'Y_COORD',
   'MAXIMUM_DURATION',
]

DATA_FILE = 'meet_the_guardians_talk.json'

SQL_FILE = 'meet_the_guardians_talk.sql'


class MeetTheGuardiansTalkSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='MeetTheGuardiansTalk',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


guardians_talks = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
