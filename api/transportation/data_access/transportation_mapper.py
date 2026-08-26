from __future__ import annotations

from .transportation_record import TransportationRecord
from ...types import Row


class TransportationMapper():
   @classmethod
   def map_record( cls, row: Row ) -> TransportationRecord:
      return TransportationRecord(
         name=row[ 'NAME' ],
         is_also_attraction=bool( row[ 'IS_ALSO_ATTRACTION' ] ),
         free_with_admission=bool( row[ 'FREE_WITH_ADMISSION' ] ),
         description=row[ 'DESCRIPTION' ],
         info_link=row[ 'INFO_LINK' ],
         hyperlink_text=row[ 'HYPERLINK_TEXT' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         region=row[ 'REGION' ],
         weekday_start_time=row[ 'WEEKDAY_START_TIME' ],
         weekday_end_time=row[ 'WEEKDAY_END_TIME' ],
         weekend_holiday_start_time=row[ 'WEEKEND_HOLIDAY_START_TIME' ],
         weekend_holiday_end_time=row[ 'WEEKEND_HOLIDAY_END_TIME' ] )


   @classmethod
   def map_records(
         cls,
         rows: list[ Row ] ) -> list[ TransportationRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
