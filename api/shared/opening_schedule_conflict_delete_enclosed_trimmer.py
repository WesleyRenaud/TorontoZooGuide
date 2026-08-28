from __future__ import annotations

from collections.abc import Callable
from datetime import date

from .opening_schedule_conflict_record import TConflict
from ..types import Connection


class OpeningScheduleConflictDeleteEnclosedTrimmer():
   @classmethod
   def try_trim(
         cls,
         conn: Connection,
         conflict: TConflict,
         *,
         conflict_start_date: date,
         conflict_end_date: date,
         new_start_date: date,
         new_end_date: date,
         delete_conflict: Callable,
   ) -> bool:
      if not (
            conflict_start_date >= new_start_date
            and conflict_end_date <= new_end_date ):
         return False

      delete_conflict( conn, conflict )
      return True
