from __future__ import annotations

from collections.abc import Callable

from .opening_schedule_conflict_record import TConflict
from .opening_schedule_conflict_resolution import OpeningScheduleConflictResolution
from .opening_schedule_input import TSchedule
from ..types import Types


class OpeningScheduleConflictResolverFactory():
   @classmethod
   def create_opening_schedule_conflict_resolver(
         cls,
         *,
         fetch_conflicts: Callable[ [ Types.Connection, TSchedule ], list[ TConflict ] ],
         delete_conflict: Callable[ [ Types.Connection, TConflict ], None ],
         insert_or_update: Callable[ [ Types.Connection, TSchedule ], None ],
         update_dates: Callable,
         insert_copy: Callable,
   ) -> OpeningScheduleConflictResolution[ TSchedule, TConflict ]:
      return OpeningScheduleConflictResolution(
         fetch_conflicts=fetch_conflicts,
         delete_conflict=delete_conflict,
         insert_or_update=insert_or_update,
         update_dates=update_dates,
         insert_copy=insert_copy )
