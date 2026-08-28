from __future__ import annotations

from collections.abc import Callable

from .opening_schedule_input import TSchedule
from ..types import Types


class OpeningScheduleConflictSaver():
   @classmethod
   def save_replacing_overlaps(
         cls,
         conn: Types.Connection,
         schedule: TSchedule,
         *,
         fetch_conflicts: Callable,
         delete_conflict: Callable,
         insert_or_update: Callable,
   ) -> bool:
      conflicts = fetch_conflicts( conn, schedule )

      for conflict in conflicts:
         delete_conflict( conn, conflict )

      insert_or_update( conn, schedule )
      conn.commit()
      return True


   @classmethod
   def save_trimming_overlaps(
         cls,
         conn: Types.Connection,
         schedule: TSchedule,
         *,
         fetch_conflicts: Callable,
         trim_conflict: Callable,
         insert_or_update: Callable,
   ) -> bool:
      conflicts = fetch_conflicts( conn, schedule )

      for conflict in conflicts:
         trim_conflict( conn, conflict, schedule )

      insert_or_update( conn, schedule )
      conn.commit()
      return True
