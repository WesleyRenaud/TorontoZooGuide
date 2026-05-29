from __future__ import annotations

from ..data_access.itinerary import fetch_itinerary_date
from ..data_access.itinerary import fetch_saved_itinerary
from .itinerary_schedule_time_order_validation import departure_follows_arrival
from ...shared.date_values import DateValues
from ...types import Connection, ScheduleTimeKey
from ...zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


def earliest_arrival_minutes(
      zoo_hours_record: ZooHoursRecord ) -> int | None:
   if zoo_hours_record.early_admission_time != None:
      return DateValues.time_value_in_minutes(
         zoo_hours_record.early_admission_time )

   return DateValues.time_value_in_minutes( zoo_hours_record.open_time )


def arrival_time_is_valid_for_zoo_hours(
      arrival_time: ScheduleTimeKey,
      zoo_hours_record: ZooHoursRecord ) -> bool:
   if arrival_time is None:
      return True

   arrival_minutes = DateValues.time_value_in_minutes( arrival_time )
   earliest_minutes = earliest_arrival_minutes( zoo_hours_record )
   last_admission_minutes = DateValues.time_value_in_minutes(
      zoo_hours_record.last_admission_time )

   return earliest_minutes <= arrival_minutes <= last_admission_minutes


def arrival_time_is_valid_for_saved_itinerary(
      conn: Connection,
      arrival_time: ScheduleTimeKey ) -> bool:
   saved_itinerary = fetch_saved_itinerary( conn )

   if not arrival_time_is_valid_for_zoo_hours(
         arrival_time,
         fetch_zoo_hours_record( conn, fetch_itinerary_date( conn ) ) ):
      return False

   return departure_follows_arrival(
      arrival_time,
      saved_itinerary.departure_time )
