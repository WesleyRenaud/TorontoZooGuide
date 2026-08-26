from __future__ import annotations

from ..data_access.wild_encounter_schedule_conflict_record import WildEncounterScheduleConflictRecord
from ..data_access.wild_encounter_schedule_provider import WildEncounterScheduleProvider
from ...shared.build_opening_schedule_conflict_resolution import OpeningScheduleConflictResolution
from ...types import Connection
from .wild_encounter_schedule_input import WildEncounterScheduleInput


_resolution = OpeningScheduleConflictResolution(
   fetch_conflicts=WildEncounterScheduleProvider.fetch_schedule_conflicts,
   delete_conflict=WildEncounterScheduleProvider.delete_schedule,
   insert_or_update=WildEncounterScheduleProvider.insert_or_update_schedule,
   update_dates=WildEncounterScheduleProvider.update_schedule_dates,
   insert_copy=WildEncounterScheduleProvider.insert_copied_schedule,
)


class WildEncounterScheduleConflictResolver():
   @classmethod
   def save_replacing_overlaps(
         cls,
         conn: Connection,
         schedule: WildEncounterScheduleInput ) -> bool:
      return _resolution.save_replacing_overlaps( conn, schedule )


   @classmethod
   def save_trimming_overlaps(
         cls,
         conn: Connection,
         schedule: WildEncounterScheduleInput ) -> bool:
      return _resolution.save_trimming_overlaps( conn, schedule )


   @classmethod
   def trim_conflict(
         cls,
         conn: Connection,
         conflict: WildEncounterScheduleConflictRecord,
         schedule: WildEncounterScheduleInput ) -> None:
      return _resolution.trim_conflict( conn, conflict, schedule )
