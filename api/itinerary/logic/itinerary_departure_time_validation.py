from __future__ import annotations

from ..data_access.itinerary import fetch_itinerary_date
from ..data_access.itinerary import fetch_saved_itinerary
from ...shared.date_values import DateValues
from ...types import Connection, ScheduleTimeKey
from ...zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord
from .itinerary_schedule_time_order_validation import departure_follows_arrival


def departure_time_is_valid_for_zoo_hours(
      departure_time: ScheduleTimeKey,
      zoo_hours_record: ZooHoursRecord ) -> bool:
   if departure_time is None:
      return True

   departure_minutes = DateValues.time_value_in_minutes( departure_time )
   open_minutes = DateValues.time_value_in_minutes( zoo_hours_record.open_time )
   close_minutes = DateValues.time_value_in_minutes( zoo_hours_record.close_time )

   return open_minutes <= departure_minutes <= close_minutes


def departure_time_is_valid_for_saved_itinerary(
      conn: Connection,
      departure_time: ScheduleTimeKey ) -> bool:
   saved_itinerary = fetch_saved_itinerary( conn )

   if not departure_time_is_valid_for_zoo_hours(
         departure_time,
         fetch_zoo_hours_record( conn, fetch_itinerary_date( conn ) ) ):
      return False

   return departure_follows_arrival(
      saved_itinerary.arrival_time,
      departure_time )
