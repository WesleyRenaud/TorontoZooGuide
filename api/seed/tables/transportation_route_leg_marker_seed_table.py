from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


RECORD_FIELDS = [
   'transportation',
   'route',
   'from_station',
   'to_station',
   'marker_id',
]

DB_COLUMNS = [
   'TRANSPORTATION',
   'ROUTE',
   'FROM_STATION',
   'TO_STATION',
   'MARKER_ID',
]

DATA_FILE = 'transportation_route_leg_marker.json'

SQL_FILE = 'transportation_route_leg_marker.sql'


class TransportationRouteLegMarkerSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Cursor ) -> None:
      JsonSeedLoader.insert_json_records(
         cursor,
         table='TransportationRouteLegMarker',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


transportation_route_leg_markers = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
