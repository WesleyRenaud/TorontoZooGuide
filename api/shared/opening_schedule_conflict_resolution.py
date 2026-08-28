from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic

from .opening_schedule_conflict_record import TConflict
from .opening_schedule_conflict_saver import OpeningScheduleConflictSaver
from .opening_schedule_conflict_trimmer import OpeningScheduleConflictTrimmer
from .opening_schedule_input import TSchedule
from ..types import Types


@dataclass( frozen=True )
class OpeningScheduleConflictResolution( Generic[ TSchedule, TConflict ] ):
   fetch_conflicts: Callable[ [ Types.Connection, TSchedule ], list[ TConflict ] ]
   delete_conflict: Callable[ [ Types.Connection, TConflict ], None ]
   insert_or_update: Callable[ [ Types.Connection, TSchedule ], None ]
   update_dates: Callable
   insert_copy: Callable

   def save_replacing_overlaps(
         self,
         conn: Types.Connection,
         schedule: TSchedule ) -> bool:
      return OpeningScheduleConflictSaver.save_replacing_overlaps(
         conn,
         schedule,
         fetch_conflicts=self.fetch_conflicts,
         delete_conflict=self.delete_conflict,
         insert_or_update=self.insert_or_update )


   def save_trimming_overlaps(
         self,
         conn: Types.Connection,
         schedule: TSchedule ) -> bool:
      return OpeningScheduleConflictSaver.save_trimming_overlaps(
         conn,
         schedule,
         fetch_conflicts=self.fetch_conflicts,
         trim_conflict=self.trim_conflict,
         insert_or_update=self.insert_or_update )


   def trim_conflict(
         self,
         conn: Types.Connection,
         conflict: TConflict,
         schedule: TSchedule ) -> None:
      OpeningScheduleConflictTrimmer.trim(
         conn,
         conflict,
         schedule,
         delete_conflict=self.delete_conflict,
         update_dates=self.update_dates,
         insert_copy=self.insert_copy )
