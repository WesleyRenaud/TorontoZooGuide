from __future__ import annotations

from .attraction_opening_schedule import AttractionOpeningSchedule
from ..data_access.attraction_schedule import delete_attraction_opening_schedule
from ..data_access.attraction_schedule import fetch_attraction_opening_schedule_conflicts
from ..data_access.attraction_schedule import insert_copied_attraction_opening_schedule
from ..data_access.attraction_schedule import insert_or_update_attraction_opening_schedule
from ..data_access.attraction_schedule import update_attraction_opening_schedule_dates
from ..data_access.attraction_schedule_record import AttractionScheduleRecord
from ...shared.opening_schedule_conflict import save_opening_schedule_replacing_overlaps
from ...shared.opening_schedule_conflict import save_opening_schedule_trimming_overlaps
from ...shared.opening_schedule_conflict import trim_opening_schedule_conflict
from ...types import Connection


def save_attraction_opening_schedule_replacing_overlaps(
      conn: Connection,
      schedule: AttractionOpeningSchedule ) -> bool:
   return save_opening_schedule_replacing_overlaps(
      conn,
      schedule,
      fetch_conflicts=fetch_attraction_opening_schedule_conflicts,
      delete_conflict=delete_attraction_opening_schedule,
      insert_or_update=insert_or_update_attraction_opening_schedule )


def save_attraction_opening_schedule_trimming_overlaps(
      conn: Connection,
      schedule: AttractionOpeningSchedule ) -> bool:
   return save_opening_schedule_trimming_overlaps(
      conn,
      schedule,
      fetch_conflicts=fetch_attraction_opening_schedule_conflicts,
      trim_conflict=trim_attraction_opening_schedule_conflict,
      insert_or_update=insert_or_update_attraction_opening_schedule )


def trim_attraction_opening_schedule_conflict(
      conn: Connection,
      conflict: AttractionScheduleRecord,
      schedule: AttractionOpeningSchedule ) -> None:
   trim_opening_schedule_conflict(
      conn,
      conflict,
      schedule,
      delete_conflict=delete_attraction_opening_schedule,
      update_dates=update_attraction_opening_schedule_dates,
      insert_copy=insert_copied_attraction_opening_schedule )


__all__ = [
   'save_attraction_opening_schedule_replacing_overlaps',
   'save_attraction_opening_schedule_trimming_overlaps',
   'trim_attraction_opening_schedule_conflict',
]
