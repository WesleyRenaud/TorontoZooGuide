from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'transportation',
   'route',
   'station',
]

DB_COLUMNS = [
   'TRANSPORTATION',
   'ROUTE',
   'STATION',
]

DATA_FILE = 'transportation_route_station.json'

SQL_FILE = 'transportation_route_station.sql'


class TransportationRouteStationSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      cursor.execute( 'DELETE FROM TransportationRouteStation;' )
      JsonSeedLoader.insert_json_records(
         cursor,
         table='TransportationRouteStation',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


transportation_route_stations = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
