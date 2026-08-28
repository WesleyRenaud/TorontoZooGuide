from __future__ import annotations

from .restaurant_schedule_record import RestaurantScheduleRecord
from ...types import Types


class RestaurantScheduleMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> RestaurantScheduleRecord:
      return RestaurantScheduleRecord(
         restaurant=row[ 'RESTAURANT' ],
         schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
         schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
         monday=row[ 'MONDAY' ],
         tuesday=row[ 'TUESDAY' ],
         wednesday=row[ 'WEDNESDAY' ],
         thursday=row[ 'THURSDAY' ],
         friday=row[ 'FRIDAY' ],
         saturday=row[ 'SATURDAY' ],
         sunday=row[ 'SUNDAY' ],
         holidays_only=row[ 'HOLIDAYS_ONLY' ],
         schedule_message=row[ 'SCHEDULE_MESSAGE' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ RestaurantScheduleRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
