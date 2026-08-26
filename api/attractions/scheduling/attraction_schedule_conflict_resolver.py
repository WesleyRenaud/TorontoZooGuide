from __future__ import annotations

from .attraction_opening_schedule import AttractionOpeningSchedule
from ..data_access.attraction_schedule_provider import AttractionScheduleProvider
from ..data_access.attraction_schedule_record import AttractionScheduleRecord
from ...shared.build_opening_schedule_conflict_resolution import OpeningScheduleConflictResolution
from ...types import Connection


_resolution = OpeningScheduleConflictResolution(
   fetch_conflicts=AttractionScheduleProvider.fetch_opening_schedule_conflicts,
   delete_conflict=AttractionScheduleProvider.delete_opening_schedule,
   insert_or_update=AttractionScheduleProvider.insert_or_update_opening_schedule,
   update_dates=AttractionScheduleProvider.update_opening_schedule_dates,
   insert_copy=AttractionScheduleProvider.insert_copied_opening_schedule,
)


class AttractionScheduleConflictResolver():
   @classmethod
   def save_replacing_overlaps(
         cls,
         conn: Connection,
         schedule: AttractionOpeningSchedule ) -> bool:
      return _resolution.save_replacing_overlaps( conn, schedule )


   @classmethod
   def save_trimming_overlaps(
         cls,
         conn: Connection,
         schedule: AttractionOpeningSchedule ) -> bool:
      return _resolution.save_trimming_overlaps( conn, schedule )


   @classmethod
   def trim_conflict(
         cls,
         conn: Connection,
         conflict: AttractionScheduleRecord,
         schedule: AttractionOpeningSchedule ) -> None:
      return _resolution.trim_conflict( conn, conflict, schedule )
