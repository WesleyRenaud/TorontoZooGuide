from __future__ import annotations

from .restaurant_closure_mapper import RestaurantClosureMapper
from .restaurant_closure_record import RestaurantClosureRecord
from ...shared.enums.position import Position
from ...types import Types


class RestaurantStatusProvider():
   @classmethod
   def save_closed_for_season(
         cls,
         conn: Types.Connection,
         restaurant: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO RestaurantStatus (
                     RESTAURANT,
                     IS_CLOSED,
                     CLOSED_MESSAGE,
                     CLOSED_START,
                     CLOSED_END,
                     CLOSED_FOR_SEASON
                  )
                  VALUES (?, 1, ?, ?, ?, 1)
                  ON CONFLICT(RESTAURANT) DO UPDATE SET
                     IS_CLOSED = 1,
                     CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                     CLOSED_START = excluded.CLOSED_START,
                     CLOSED_END = excluded.CLOSED_END,
                     CLOSED_FOR_SEASON = 1;
            """,
            (
               restaurant,
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
         restaurant: str ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   DELETE FROM RestaurantStatus
                  WHERE RESTAURANT = ?
                     AND CLOSED_FOR_SEASON = 1;
            """,
            ( restaurant, ) )

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
                     RESTAURANT
                  FROM RestaurantStatus
                  WHERE IS_CLOSED = 1
                     AND CLOSED_FOR_SEASON = 1
                     AND (
                        CLOSED_END IS NULL
                        OR CLOSED_END >= ?
                     )
                  ORDER BY RESTAURANT;
            """,
            ( today, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()


   @classmethod
   def fetch_closure_record(
         cls,
         conn: Types.Connection,
         restaurant: str ) -> RestaurantClosureRecord | None:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT
                     RESTAURANT,
                     CLOSED_START,
                     CLOSED_END,
                     CLOSED_MESSAGE,
                     CLOSED_FOR_SEASON
                  FROM RestaurantStatus
                  WHERE RESTAURANT = ?
                     AND IS_CLOSED = 1
                     AND CLOSED_FOR_SEASON = 1;
            """,
            ( restaurant, ) ).fetchone()

         if row == None:
            return None

         return RestaurantClosureMapper.map_record( row )

      finally:
         cur.close()


   @classmethod
   def fetch_closure_records( cls, conn: Types.Connection ) -> list[ RestaurantClosureRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     RESTAURANT,
                     CLOSED_START,
                     CLOSED_END,
                     CLOSED_MESSAGE,
                     CLOSED_FOR_SEASON
                  FROM RestaurantStatus
                  WHERE IS_CLOSED = 1
                     AND CLOSED_FOR_SEASON = 1;
            """ )

         return RestaurantClosureMapper.map_records( data.fetchall() )

      finally:
         cur.close()
