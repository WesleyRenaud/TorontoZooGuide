from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'species',
   'exhibit',
   'name',
   'enclosure_type',
   'seasonally_off_display_message',
   'x_coord',
   'y_coord',
   'default_itinerary_duration_minutes',
   'is_zoomobile_only',
]

DB_COLUMNS = [
   'SPECIES',
   'EXHIBIT',
   'NAME',
   'ENCLOSURE_TYPE',
   'SEASONALLY_OFF_DISPLAY_MESSAGE',
   'X_COORD',
   'Y_COORD',
   'DEFAULT_ITINERARY_DURATION_MINUTES',
   'IS_ZOOMOBILE_ONLY',
]

DATA_FILE = 'enclosure_viewing.json'

SQL_FILE = 'enclosure_viewing.sql'


class EnclosureViewingSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='EnclosureViewing',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


enclosure_viewings = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
