from __future__ import annotations

from collections.abc import Callable
from datetime import date
from datetime import timedelta

from .opening_schedule_conflict_record import TConflict
from .opening_schedule_date_resolver import OpeningScheduleDateResolver
from ..types import Connection


class OpeningScheduleConflictShortenEndTrimmer():
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
         conflict_start_attr: str,
         update_dates: Callable,
   ) -> bool:
      if not (
            conflict_start_date < new_start_date
            and conflict_end_date <= new_end_date ):
         return False

      update_dates(
         conn,
         conflict,
         start_date=getattr( conflict, conflict_start_attr ),
         end_date=OpeningScheduleDateResolver.format_date(
            new_start_date - timedelta( days=1 ) ) )

      return True
