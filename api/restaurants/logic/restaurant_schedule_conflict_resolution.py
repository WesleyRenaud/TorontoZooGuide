from __future__ import annotations

from ..data_access.restaurant_schedule import delete_restaurant_opening_schedule
from ..data_access.restaurant_schedule import fetch_restaurant_opening_schedule_conflicts
from ..data_access.restaurant_schedule import insert_copied_restaurant_opening_schedule
from ..data_access.restaurant_schedule import insert_or_update_restaurant_opening_schedule
from ..data_access.restaurant_schedule import update_restaurant_opening_schedule_dates
from ..data_access.restaurant_schedule_record import RestaurantScheduleRecord
from .restaurant_opening_schedule import RestaurantOpeningSchedule
from ...shared.opening_schedule_conflict import save_opening_schedule_replacing_overlaps
from ...shared.opening_schedule_conflict import save_opening_schedule_trimming_overlaps
from ...shared.opening_schedule_conflict import trim_opening_schedule_conflict
from ...shared.opening_schedule_dates import format_opening_schedule_date
from ...shared.opening_schedule_dates import parse_opening_schedule_end_date
from ...types import Connection


def save_restaurant_opening_schedule_replacing_overlaps(
      conn: Connection,
      schedule: RestaurantOpeningSchedule ) -> bool:
   return save_opening_schedule_replacing_overlaps(
      conn,
      schedule,
      fetch_conflicts=fetch_restaurant_opening_schedule_conflicts,
      delete_conflict=delete_restaurant_opening_schedule,
      insert_or_update=insert_or_update_restaurant_opening_schedule )


def save_restaurant_opening_schedule_trimming_overlaps(
      conn: Connection,
      schedule: RestaurantOpeningSchedule ) -> bool:
   return save_opening_schedule_trimming_overlaps(
      conn,
      schedule,
      fetch_conflicts=fetch_restaurant_opening_schedule_conflicts,
      trim_conflict=trim_restaurant_opening_schedule_conflict,
      insert_or_update=insert_or_update_restaurant_opening_schedule )


def trim_restaurant_opening_schedule_conflict(
      conn: Connection,
      conflict: RestaurantScheduleRecord,
      schedule: RestaurantOpeningSchedule ) -> None:
   trim_opening_schedule_conflict(
      conn,
      conflict,
      schedule,
      delete_conflict=delete_restaurant_opening_schedule,
      update_dates=update_restaurant_opening_schedule_dates,
      insert_copy=insert_copied_restaurant_opening_schedule )


__all__ = [
   'format_opening_schedule_date',
   'parse_opening_schedule_end_date',
   'save_restaurant_opening_schedule_replacing_overlaps',
   'save_restaurant_opening_schedule_trimming_overlaps',
   'trim_restaurant_opening_schedule_conflict',
]
