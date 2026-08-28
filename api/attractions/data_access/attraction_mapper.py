from __future__ import annotations

from .attraction_record import AttractionRecord
from ...types import Types


class AttractionMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AttractionRecord:
      return AttractionRecord(
         name=row[ 'NAME' ],
         free_with_admission=row[ 'FREE_WITH_ADMISSION' ],
         description=row[ 'DESCRIPTION' ],
         info_link=row[ 'INFO_LINK' ],
         hyperlink_text=row[ 'HYPERLINK_TEXT' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         region=row[ 'REGION' ],
         weekday_multiplier=row[ 'ATTRACTION_DAY_SEASONAL_WEEKDAY_MULTIPLIER' ],
         weekend_holiday_multiplier=row[ 'ATTRACTION_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER' ],
         weekday_start_time=row[ 'WEEKDAY_START_TIME' ],
         weekday_end_time=row[ 'WEEKDAY_END_TIME' ],
         weekend_holiday_start_time=row[ 'WEEKEND_HOLIDAY_START_TIME' ],
         weekend_holiday_end_time=row[ 'WEEKEND_HOLIDAY_END_TIME' ],
         is_also_transportation=bool( row[ 'IS_ALSO_TRANSPORTATION' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ AttractionRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
