from __future__ import annotations

from datetime import date
from datetime import timedelta

from .attraction_opening_schedule import AttractionOpeningSchedule
from ..data_access.attraction_schedule import delete_attraction_opening_schedule
from ..data_access.attraction_schedule import fetch_attraction_opening_schedule_conflicts
from ..data_access.attraction_schedule import insert_copied_attraction_opening_schedule
from ..data_access.attraction_schedule import insert_or_update_attraction_opening_schedule
from ..data_access.attraction_schedule import update_attraction_opening_schedule_dates
from ..data_access.attraction_schedule_record import AttractionScheduleRecord
from ...shared.date_values import DateValues
from ...types import Connection, DateInput, DateKey


def save_attraction_opening_schedule_replacing_overlaps(
      conn: Connection,
      schedule: AttractionOpeningSchedule ) -> bool:
   conflicts = fetch_attraction_opening_schedule_conflicts( conn, schedule )

   for conflict in conflicts:
      delete_attraction_opening_schedule( conn, conflict )

   insert_or_update_attraction_opening_schedule( conn, schedule )
   conn.commit()
   return True


def save_attraction_opening_schedule_trimming_overlaps(
      conn: Connection,
      schedule: AttractionOpeningSchedule ) -> bool:
   conflicts = fetch_attraction_opening_schedule_conflicts( conn, schedule )

   for conflict in conflicts:
      trim_attraction_opening_schedule_conflict( conn, conflict, schedule )

   insert_or_update_attraction_opening_schedule( conn, schedule )
   conn.commit()
   return True


def trim_attraction_opening_schedule_conflict(
      conn: Connection,
      conflict: AttractionScheduleRecord,
      schedule: AttractionOpeningSchedule ) -> None:
   new_start_date = DateValues.parse_date_value( schedule.start_date )
   new_end_date = parse_opening_schedule_end_date( schedule.end_date )
   conflict_start_date = DateValues.parse_date_value( conflict.schedule_start_date )
   conflict_end_date = parse_opening_schedule_end_date(
      conflict.schedule_end_date )

   if conflict_start_date >= new_start_date and conflict_end_date <= new_end_date:
      delete_attraction_opening_schedule( conn, conflict )
      return

   if conflict_start_date < new_start_date and conflict_end_date <= new_end_date:
      update_attraction_opening_schedule_dates(
         conn,
         conflict,
         start_date=conflict.schedule_start_date,
         end_date=format_opening_schedule_date(
            new_start_date - timedelta( days=1 ) ) )
      return

   if conflict_start_date >= new_start_date and conflict_end_date > new_end_date:
      update_attraction_opening_schedule_dates(
         conn,
         conflict,
         start_date=format_opening_schedule_date(
            new_end_date + timedelta( days=1 ) ),
         end_date=conflict.schedule_end_date )
      return

   update_attraction_opening_schedule_dates(
      conn,
      conflict,
      start_date=conflict.schedule_start_date,
      end_date=format_opening_schedule_date(
         new_start_date - timedelta( days=1 ) ) )

   if new_end_date == date.max:
      return

   insert_copied_attraction_opening_schedule(
      conn,
      conflict,
      start_date=format_opening_schedule_date(
         new_end_date + timedelta( days=1 ) ),
      end_date=conflict.schedule_end_date )


def parse_opening_schedule_end_date( value: DateInput ) -> date:
   if value == None:
      return date.max

   return DateValues.parse_date_value( value )


def format_opening_schedule_date( value: date ) -> DateKey | None:
   if value == date.max:
      return None

   return value.isoformat()
