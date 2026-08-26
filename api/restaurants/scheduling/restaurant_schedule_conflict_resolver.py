from __future__ import annotations

from ..data_access.restaurant_schedule_provider import RestaurantScheduleProvider
from ..data_access.restaurant_schedule_record import RestaurantScheduleRecord
from .restaurant_opening_schedule import RestaurantOpeningSchedule
from ...shared.build_opening_schedule_conflict_resolution import OpeningScheduleConflictResolution
from ...types import Connection


_resolution = OpeningScheduleConflictResolution(
   fetch_conflicts=RestaurantScheduleProvider.fetch_opening_schedule_conflicts,
   delete_conflict=RestaurantScheduleProvider.delete_opening_schedule,
   insert_or_update=RestaurantScheduleProvider.insert_or_update_opening_schedule,
   update_dates=RestaurantScheduleProvider.update_opening_schedule_dates,
   insert_copy=RestaurantScheduleProvider.insert_copied_opening_schedule,
)


class RestaurantScheduleConflictResolver():
   @classmethod
   def save_replacing_overlaps(
         cls,
         conn: Connection,
         schedule: RestaurantOpeningSchedule ) -> bool:
      return _resolution.save_replacing_overlaps( conn, schedule )


   @classmethod
   def save_trimming_overlaps(
         cls,
         conn: Connection,
         schedule: RestaurantOpeningSchedule ) -> bool:
      return _resolution.save_trimming_overlaps( conn, schedule )


   @classmethod
   def trim_conflict(
         cls,
         conn: Connection,
         conflict: RestaurantScheduleRecord,
         schedule: RestaurantOpeningSchedule ) -> None:
      return _resolution.trim_conflict( conn, conflict, schedule )
