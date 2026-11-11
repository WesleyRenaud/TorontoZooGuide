from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'name',
   'free_with_admission',
   'description',
   'info_link',
   'hyperlink_text',
   'x_coord',
   'y_coord',
   'default_itinerary_duration_minutes',
   'region',
   'is_also_transportation',
   'closed_for_season_until_month',
   'weekday_start_month',
   'weekday_end_month',
   'weekend_start_month',
   'weekend_end_month',
]

DB_COLUMNS = [
   'NAME',
   'FREE_WITH_ADMISSION',
   'DESCRIPTION',
   'INFO_LINK',
   'HYPERLINK_TEXT',
   'X_COORD',
   'Y_COORD',
   'DEFAULT_ITINERARY_DURATION_MINUTES',
   'REGION',
   'IS_ALSO_TRANSPORTATION',
   'CLOSED_FOR_SEASON_UNTIL_MONTH',
   'WEEKDAY_START_MONTH',
   'WEEKDAY_END_MONTH',
   'WEEKEND_START_MONTH',
   'WEEKEND_END_MONTH',
]

DATA_FILE = 'attraction.json'

SQL_FILE = 'attraction.sql'


class AttractionSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='Attraction',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


attractions = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
