from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'name',
   'x_coord',
   'y_coord',
   'loop_id',
   'loop_viewing_spot_index',
   'region',
]

DB_COLUMNS = [
   'NAME',
   'X_COORD',
   'Y_COORD',
   'LOOP_ID',
   'LOOP_VIEWING_SPOT_INDEX',
   'REGION',
]

DATA_FILE = 'wild_encounter_meeting_spot.json'

SQL_FILE = 'wild_encounter_meeting_spot.sql'


class WildEncounterMeetingSpotSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='WildEncounterMeetingSpot',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


wild_encounter_meeting_spots = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
