from __future__ import annotations

from ...types import Row
from .zoo_hours_record import ZooHoursRecord


class ZooHoursMapper():
   @classmethod
   def map_record( cls, row: Row ) -> ZooHoursRecord:
      return ZooHoursRecord(
         operating_date=row[ 'OPERATING_DATE' ],
         early_admission_time=row[ 'EARLY_ADMISSION_TIME' ],
         open_time=row[ 'OPEN_TIME' ],
         last_admission_time=row[ 'LAST_ADMISSION_TIME' ],
         close_time=row[ 'CLOSE_TIME' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ ZooHoursRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
