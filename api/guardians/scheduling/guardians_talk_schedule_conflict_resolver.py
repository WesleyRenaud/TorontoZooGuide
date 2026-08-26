from __future__ import annotations

from ..data_access.guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from ..data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from .guardians_talk_schedule_input import GuardiansTalkScheduleInput
from ...shared.build_opening_schedule_conflict_resolution import OpeningScheduleConflictResolution
from ...types import Connection


_resolution = OpeningScheduleConflictResolution(
   fetch_conflicts=GuardiansTalkScheduleProvider.fetch_schedule_conflicts,
   delete_conflict=GuardiansTalkScheduleProvider.delete_schedule,
   insert_or_update=GuardiansTalkScheduleProvider.insert_or_update_schedule,
   update_dates=GuardiansTalkScheduleProvider.update_schedule_dates,
   insert_copy=GuardiansTalkScheduleProvider.insert_copied_schedule,
)


class GuardiansTalkScheduleConflictResolver():
   @classmethod
   def save_replacing_overlaps(
         cls,
         conn: Connection,
         schedule: GuardiansTalkScheduleInput ) -> bool:
      return _resolution.save_replacing_overlaps( conn, schedule )


   @classmethod
   def save_trimming_overlaps(
         cls,
         conn: Connection,
         schedule: GuardiansTalkScheduleInput ) -> bool:
      return _resolution.save_trimming_overlaps( conn, schedule )


   @classmethod
   def trim_conflict(
         cls,
         conn: Connection,
         conflict: GuardiansTalkScheduleRecord,
         schedule: GuardiansTalkScheduleInput ) -> None:
      return _resolution.trim_conflict( conn, conflict, schedule )
