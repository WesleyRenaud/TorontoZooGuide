from __future__ import annotations

from .attraction_hours_schedule import AttractionHoursSchedule
from ..data_access.attraction_hours_schedule_provider import AttractionHoursScheduleProvider
from ..data_access.attraction_hours_schedule_record import AttractionHoursScheduleRecord
from ...shared.build_opening_schedule_conflict_resolution import OpeningScheduleConflictResolution
from ...types import Connection


_resolution = OpeningScheduleConflictResolution(
   fetch_conflicts=AttractionHoursScheduleProvider.fetch_hours_schedule_conflicts,
   delete_conflict=AttractionHoursScheduleProvider.delete_hours_schedule,
   insert_or_update=AttractionHoursScheduleProvider.insert_or_update_hours_schedule,
   update_dates=AttractionHoursScheduleProvider.update_hours_schedule_dates,
   insert_copy=AttractionHoursScheduleProvider.insert_copied_hours_schedule,
)


class AttractionHoursScheduleConflictResolver():
   @classmethod
   def save_replacing_overlaps(
         cls,
         conn: Connection,
         schedule: AttractionHoursSchedule ) -> bool:
      return _resolution.save_replacing_overlaps( conn, schedule )


   @classmethod
   def save_trimming_overlaps(
         cls,
         conn: Connection,
         schedule: AttractionHoursSchedule ) -> bool:
      return _resolution.save_trimming_overlaps( conn, schedule )


   @classmethod
   def trim_conflict(
         cls,
         conn: Connection,
         conflict: AttractionHoursScheduleRecord,
         schedule: AttractionHoursSchedule ) -> None:
      return _resolution.trim_conflict( conn, conflict, schedule )
