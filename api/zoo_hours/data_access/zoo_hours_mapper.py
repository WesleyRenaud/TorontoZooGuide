from __future__ import annotations

from ...types import Row
from .zoo_hours_record import ZooHoursRecord


def map_zoo_hours_record( row: Row ) -> ZooHoursRecord:
   return ZooHoursRecord(
      operating_date=row[ 'OPERATING_DATE' ],
      early_admission_time=row[ 'EARLY_ADMISSION_TIME' ],
      open_time=row[ 'OPEN_TIME' ],
      last_admission_time=row[ 'LAST_ADMISSION_TIME' ],
      close_time=row[ 'CLOSE_TIME' ] )
