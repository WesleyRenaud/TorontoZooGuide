from __future__ import annotations

from ..json_seed_loader import JsonSeedLoader
from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


RECORD_FIELDS = [
   'transportation',
   'route',
]

DB_COLUMNS = [
   'TRANSPORTATION',
   'ROUTE',
]

DATA_FILE = 'transportation_route.json'

SQL_FILE = 'transportation_route.sql'


class TransportationRouteSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )


   @classmethod
   def insert_rows( cls, cursor: Types.Cursor ) -> None:
      cursor.execute( 'DELETE FROM TransportationRoute;' )
      JsonSeedLoader.insert_json_records(
         cursor,
         table='TransportationRoute',
         columns=DB_COLUMNS,
         fields=RECORD_FIELDS,
         path=JsonSeedLoader.seed_data_path( DATA_FILE ) )


transportation_routes = JsonSeedLoader.load_json_records(
   JsonSeedLoader.seed_data_path( DATA_FILE ),
   fields=RECORD_FIELDS )
