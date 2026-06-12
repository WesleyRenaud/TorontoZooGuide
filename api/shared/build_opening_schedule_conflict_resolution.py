from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic

from .opening_schedule_conflict import save_opening_schedule_replacing_overlaps
from .opening_schedule_conflict import save_opening_schedule_trimming_overlaps
from .opening_schedule_conflict import trim_opening_schedule_conflict
from .opening_schedule_conflict_record import TConflict
from .opening_schedule_input import TSchedule
from ..types import Connection


@dataclass( frozen=True )
class OpeningScheduleConflictResolution( Generic[ TSchedule, TConflict ] ):
   fetch_conflicts: Callable[ [ Connection, TSchedule ], list[ TConflict ] ]
   delete_conflict: Callable[ [ Connection, TConflict ], None ]
   insert_or_update: Callable[ [ Connection, TSchedule ], None ]
   update_dates: Callable
   insert_copy: Callable

   def save_replacing_overlaps(
         self,
         conn: Connection,
         schedule: TSchedule ) -> bool:
      return save_opening_schedule_replacing_overlaps(
         conn,
         schedule,
         fetch_conflicts=self.fetch_conflicts,
         delete_conflict=self.delete_conflict,
         insert_or_update=self.insert_or_update )


   def save_trimming_overlaps(
         self,
         conn: Connection,
         schedule: TSchedule ) -> bool:
      return save_opening_schedule_trimming_overlaps(
         conn,
         schedule,
         fetch_conflicts=self.fetch_conflicts,
         trim_conflict=self.trim_conflict,
         insert_or_update=self.insert_or_update )


   def trim_conflict(
         self,
         conn: Connection,
         conflict: TConflict,
         schedule: TSchedule ) -> None:
      trim_opening_schedule_conflict(
         conn,
         conflict,
         schedule,
         delete_conflict=self.delete_conflict,
         update_dates=self.update_dates,
         insert_copy=self.insert_copy )
