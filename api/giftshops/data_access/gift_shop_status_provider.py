from __future__ import annotations

from .gift_shop_closure_mapper import GiftShopClosureMapper
from .gift_shop_closure_record import GiftShopClosureRecord
from ...shared.enums.position import Position
from ...types import Types


class GiftShopStatusProvider():
   @classmethod
   def save_closed_for_season(
         cls,
         conn: Types.Connection,
         gift_shop: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO GiftShopStatus (
                     GIFT_SHOP,
                     IS_CLOSED,
                     CLOSED_MESSAGE,
                     CLOSED_START,
                     CLOSED_END,
                     CLOSED_FOR_SEASON
                  )
                  VALUES (?, 1, ?, ?, ?, 1)
                  ON CONFLICT(GIFT_SHOP) DO UPDATE SET
                     IS_CLOSED = 1,
                     CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                     CLOSED_START = excluded.CLOSED_START,
                     CLOSED_END = excluded.CLOSED_END,
                     CLOSED_FOR_SEASON = 1;
            """,
            (
               gift_shop,
               message,
               start_date,
               end_date,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def delete_closed_for_season(
         cls,
         conn: Types.Connection,
         gift_shop: str ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   DELETE FROM GiftShopStatus
                  WHERE GIFT_SHOP = ?
                     AND CLOSED_FOR_SEASON = 1;
            """,
            ( gift_shop, ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def fetch_closed_for_season_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     GIFT_SHOP
                  FROM GiftShopStatus
                  WHERE IS_CLOSED = 1
                     AND CLOSED_FOR_SEASON = 1
                     AND (
                        CLOSED_END IS NULL
                        OR CLOSED_END >= ?
                     )
                  ORDER BY GIFT_SHOP;
            """,
            ( today, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()


   @classmethod
   def fetch_closure_record(
         cls,
         conn: Types.Connection,
         gift_shop: str ) -> GiftShopClosureRecord | None:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT
                     GIFT_SHOP,
                     CLOSED_START,
                     CLOSED_END,
                     CLOSED_MESSAGE,
                     CLOSED_FOR_SEASON
                  FROM GiftShopStatus
                  WHERE GIFT_SHOP = ?
                     AND IS_CLOSED = 1
                     AND CLOSED_FOR_SEASON = 1;
            """,
            ( gift_shop, ) ).fetchone()

         if row == None:
            return None

         return GiftShopClosureMapper.map_record( row )

      finally:
         cur.close()


   @classmethod
   def fetch_closure_records( cls, conn: Types.Connection ) -> list[ GiftShopClosureRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     GIFT_SHOP,
                     CLOSED_START,
                     CLOSED_END,
                     CLOSED_MESSAGE,
                     CLOSED_FOR_SEASON
                  FROM GiftShopStatus
                  WHERE IS_CLOSED = 1
                     AND CLOSED_FOR_SEASON = 1;
            """ )

         return GiftShopClosureMapper.map_records( data.fetchall() )

      finally:
         cur.close()
