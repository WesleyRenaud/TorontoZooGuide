from __future__ import annotations

from dataclasses import replace
from datetime import date

from ....attractions.scheduling.attraction_operating_hours import fetch_configured_attraction_operating_hours_seconds
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from .loop_pin_segments import viewing_spot_index_for_stop_in_loop
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_unit import LoopScheduleUnit
from ...routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ....types import DateKey


def resolve_attraction_hours_soft_pins(
      conn: Connection,
      *,
      attractions: list[ ItineraryAttractionRecord ],
      loop_units: list[ LoopScheduleUnit ],
      visit_date: date | DateKey,
      zoo_open_seconds: int,
      zoo_close_seconds: int,
   ) -> list[ AttractionHoursSoftPin ]:
   parsed_visit_date = DateValues.parse_date_value( visit_date )

   if parsed_visit_date is None:
      return []

   loop_id_by_attraction_name = _loop_id_by_attraction_name( loop_units )
   soft_pins: list[ AttractionHoursSoftPin ] = []

   for attraction_row in attractions:
      loop_id = loop_id_by_attraction_name.get( attraction_row.attraction )

      if loop_id is None:
         continue

      attraction_hours = fetch_configured_attraction_operating_hours_seconds(
         conn,
         attraction_row.attraction,
         visit_date=parsed_visit_date,
         zoo_open_seconds=zoo_open_seconds,
         zoo_close_seconds=zoo_close_seconds )

      if attraction_hours is None:
         continue

      open_seconds, close_seconds = attraction_hours

      if open_seconds >= close_seconds:
         continue

      viewing_spot_index = viewing_spot_index_for_stop_in_loop(
         loop_id,
         attraction_row )

      if viewing_spot_index is None:
         continue

      soft_pins.append(
         AttractionHoursSoftPin(
            loop_id=loop_id,
            viewing_spot_index=viewing_spot_index,
            attraction_name=attraction_row.attraction,
            open_seconds=open_seconds,
            close_seconds=close_seconds ) )

   soft_pins.sort(
      key=lambda soft_pin: (
         soft_pin.open_seconds,
         soft_pin.viewing_spot_index,
         soft_pin.attraction_name ) )
   return soft_pins


def attach_attraction_hours_soft_pins_to_schedule_windows(
      schedule_windows: list[ ItineraryScheduleWindow ],
      soft_pins: list[ AttractionHoursSoftPin ],
   ) -> list[ ItineraryScheduleWindow ]:
   if not soft_pins:
      return schedule_windows

   return [
      replace(
         schedule_window,
         attraction_hours_soft_pins=[
            soft_pin
            for soft_pin in soft_pins
            if _soft_pin_applies_to_schedule_window(
               soft_pin,
               schedule_window )
         ] )
      for schedule_window in schedule_windows
   ]


def attraction_hours_by_name_from_soft_pins(
      soft_pins: list[ AttractionHoursSoftPin ],
   ) -> dict[ str, tuple[ int, int ] ]:
   return {
      soft_pin.attraction_name: (
         soft_pin.open_seconds,
         soft_pin.close_seconds )
      for soft_pin in soft_pins
   }


def _soft_pin_applies_to_schedule_window(
      soft_pin: AttractionHoursSoftPin,
      schedule_window: ItineraryScheduleWindow ) -> bool:
   return (
      soft_pin.open_seconds < schedule_window.end_seconds
      and soft_pin.close_seconds > schedule_window.start_seconds
   )


def _loop_id_by_attraction_name(
      loop_units: list[ LoopScheduleUnit ],
   ) -> dict[ str, str ]:
   loop_ids: dict[ str, str ] = {}

   for loop_unit in loop_units:
      if loop_unit.loop_id is None:
         continue

      for stop in loop_unit.stops:
         if not isinstance( stop, ItineraryAttractionRecord ):
            continue

         loop_ids[ stop.attraction ] = loop_unit.loop_id

   return loop_ids


def stops_before_attraction_hours_soft_pin(
      stops: list[ LoopScheduleStop ],
      *,
      loop_id: str,
      soft_pin: AttractionHoursSoftPin,
   ) -> list[ LoopScheduleStop ]:
   before_stops: list[ LoopScheduleStop ] = []

   for stop in stops:
      stop_index = viewing_spot_index_for_stop_in_loop( loop_id, stop )

      if stop_index is None:
         continue

      if stop_index < soft_pin.viewing_spot_index:
         before_stops.append( stop )

   return before_stops
