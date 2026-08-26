from __future__ import annotations

from .restaurant_schedule_override_record import RestaurantScheduleOverrideRecord
from ...types import Row


class RestaurantScheduleOverrideMapper():
   @classmethod
   def map_record( cls, row: Row ) -> RestaurantScheduleOverrideRecord:
      return RestaurantScheduleOverrideRecord(
         restaurant=row[ 'RESTAURANT' ],
         override_start_date=row[ 'OVERRIDE_START_DATE' ],
         override_end_date=row[ 'OVERRIDE_END_DATE' ],
         is_closed=row[ 'IS_CLOSED' ],
         override_message=row[ 'OVERRIDE_MESSAGE' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ RestaurantScheduleOverrideRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
