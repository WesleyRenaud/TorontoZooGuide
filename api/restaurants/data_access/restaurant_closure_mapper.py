from __future__ import annotations

from .restaurant_closure_record import RestaurantClosureRecord
from ...types import Types


class RestaurantClosureMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> RestaurantClosureRecord:
      return RestaurantClosureRecord(
         restaurant=row[ 'RESTAURANT' ],
         closed_start=row[ 'CLOSED_START' ],
         closed_end=row[ 'CLOSED_END' ],
         closed_message=row[ 'CLOSED_MESSAGE' ],
         is_closed_for_season=bool( row[ 'CLOSED_FOR_SEASON' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ RestaurantClosureRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
