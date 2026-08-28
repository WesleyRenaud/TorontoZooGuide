from __future__ import annotations

from ..seed_sql_loader import SeedSqlLoader
from ...types import Cursor


SQL_FILE = 'gift_shop_opening_schedule.sql'


class GiftShopOpeningScheduleSeedTable():
   @classmethod
   def create_table( cls, cursor: Cursor ) -> None:
      SeedSqlLoader.execute_sql_file( cursor, SeedSqlLoader.seed_sql_path( SQL_FILE ) )
