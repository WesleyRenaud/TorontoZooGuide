from __future__ import annotations

from ..seed_sql_loader import SeedSqlLoader
from ...types import Types


SQL_FILE = 'itinerary_exhibit.sql'


class ItineraryExhibitSeedTable():
   @classmethod
   def create_table( cls, cursor: Types.Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )
