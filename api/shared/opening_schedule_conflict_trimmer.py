from __future__ import annotations

from collections.abc import Callable

from .calendar_dates import DateValues
from .opening_schedule_conflict_delete_enclosed_trimmer import OpeningScheduleConflictDeleteEnclosedTrimmer
from .opening_schedule_conflict_record import TConflict
from .opening_schedule_conflict_shorten_end_trimmer import OpeningScheduleConflictShortenEndTrimmer
from .opening_schedule_conflict_shorten_start_trimmer import OpeningScheduleConflictShortenStartTrimmer
from .opening_schedule_conflict_split_wrap_trimmer import OpeningScheduleConflictSplitWrapTrimmer
from .opening_schedule_date_resolver import OpeningScheduleDateResolver
from .opening_schedule_input import TSchedule
from ..types import Types


class OpeningScheduleConflictTrimmer():
   @classmethod
   def trim(
         cls,
         conn: Types.Connection,
         conflict: TConflict,
         schedule: TSchedule,
         *,
         delete_conflict: Callable,
         update_dates: Callable,
         insert_copy: Callable,
         conflict_start_attr: str = 'schedule_start_date',
         conflict_end_attr: str = 'schedule_end_date',
         new_start_attr: str = 'start_date',
         new_end_attr: str = 'end_date',
   ) -> None:
      new_start_date = DateValues.parse_date_value(
         getattr( schedule, new_start_attr ) )
      new_end_date = OpeningScheduleDateResolver.parse_end_date(
         getattr( schedule, new_end_attr ) )
      conflict_start_date = DateValues.parse_date_value(
         getattr( conflict, conflict_start_attr ) )
      conflict_end_date = OpeningScheduleDateResolver.parse_end_date(
         getattr( conflict, conflict_end_attr ) )

      if OpeningScheduleConflictDeleteEnclosedTrimmer.try_trim(
            conn,
            conflict,
            conflict_start_date=conflict_start_date,
            conflict_end_date=conflict_end_date,
            new_start_date=new_start_date,
            new_end_date=new_end_date,
            delete_conflict=delete_conflict ):
         return

      if OpeningScheduleConflictShortenEndTrimmer.try_trim(
            conn,
            conflict,
            conflict_start_date=conflict_start_date,
            conflict_end_date=conflict_end_date,
            new_start_date=new_start_date,
            new_end_date=new_end_date,
            conflict_start_attr=conflict_start_attr,
            update_dates=update_dates ):
         return

      if OpeningScheduleConflictShortenStartTrimmer.try_trim(
            conn,
            conflict,
            conflict_start_date=conflict_start_date,
            conflict_end_date=conflict_end_date,
            new_start_date=new_start_date,
            new_end_date=new_end_date,
            conflict_end_attr=conflict_end_attr,
            update_dates=update_dates ):
         return

      OpeningScheduleConflictSplitWrapTrimmer.trim(
         conn,
         conflict,
         new_start_date=new_start_date,
         new_end_date=new_end_date,
         conflict_start_attr=conflict_start_attr,
         conflict_end_attr=conflict_end_attr,
         update_dates=update_dates,
         insert_copy=insert_copy )
