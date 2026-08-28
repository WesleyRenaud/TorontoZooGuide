from __future__ import annotations

from dataclasses import replace
from datetime import date

from ....attractions.scheduling.attraction_operating_hours_resolver import AttractionOperatingHoursResolver
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from .loop_pin_segment_splitter import LoopPinSegmentSplitter
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_unit import LoopScheduleUnit
from ...routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from ...routing.itinerary_schedule_window import ItineraryScheduleWindow
from ....shared.calendar_dates import DateValues
from ....shared.operating_hours import OperatingHours
from ....types import Types


AttractionHoursSoftPinStop = (
   ItineraryAttractionRecord
   | ItineraryTransportationRecord
)


class AttractionHoursSoftPinResolver():
   @classmethod
   def resolve(
         cls,
         conn: Types.Connection,
         *,
         attractions: list[ AttractionHoursSoftPinStop ],
         loop_units: list[ LoopScheduleUnit ],
         visit_date: date | Types.DateKey,
         zoo_operating_hours: OperatingHours,
      ) -> list[ AttractionHoursSoftPin ]:
      parsed_visit_date = DateValues.parse_date_value( visit_date )

      if parsed_visit_date is None:
         return []

      loop_id_by_attraction_name = cls._loop_id_by_attraction_name( loop_units )
      soft_pins: list[ AttractionHoursSoftPin ] = []

      for attraction_row in attractions:
         loop_id = loop_id_by_attraction_name.get( attraction_row.attraction )

         if loop_id is None:
            continue

         attraction_hours = AttractionOperatingHoursResolver.fetch_configured_operating_hours_seconds(
            conn,
            attraction_row.attraction,
            visit_date=parsed_visit_date,
            zoo_operating_hours=zoo_operating_hours )

         if attraction_hours is None:
            continue

         if attraction_hours.open_seconds >= attraction_hours.close_seconds:
            continue

         viewing_spot_index = LoopPinSegmentSplitter.viewing_spot_index_for_stop(
            loop_id,
            attraction_row )

         if viewing_spot_index is None:
            continue

         soft_pins.append(
            AttractionHoursSoftPin(
               loop_id=loop_id,
               viewing_spot_index=viewing_spot_index,
               attraction_name=attraction_row.attraction,
               open_seconds=attraction_hours.open_seconds,
               close_seconds=attraction_hours.close_seconds ) )

      soft_pins.sort(
         key=lambda soft_pin: (
            soft_pin.open_seconds,
            soft_pin.viewing_spot_index,
            soft_pin.attraction_name ) )
      return soft_pins


   @classmethod
   def attach_to_windows(
         cls,
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
               if cls._applies_to_window( soft_pin, schedule_window )
            ] )
         for schedule_window in schedule_windows
      ]


   @classmethod
   def hours_by_name(
         cls,
         soft_pins: list[ AttractionHoursSoftPin ],
      ) -> dict[ str, OperatingHours ]:
      return {
         soft_pin.attraction_name: OperatingHours(
            open_seconds=soft_pin.open_seconds,
            close_seconds=soft_pin.close_seconds )
         for soft_pin in soft_pins
      }


   @classmethod
   def stops_before(
         cls,
         stops: list[ LoopScheduleStop.Stop ],
         *,
         loop_id: str,
         soft_pin: AttractionHoursSoftPin,
      ) -> list[ LoopScheduleStop.Stop ]:
      before_stops: list[ LoopScheduleStop.Stop ] = []

      for stop in stops:
         stop_index = LoopPinSegmentSplitter.viewing_spot_index_for_stop(
            loop_id,
            stop )

         if stop_index is None:
            continue

         if stop_index < soft_pin.viewing_spot_index:
            before_stops.append( stop )

      return before_stops


   @classmethod
   def _applies_to_window(
         cls,
         soft_pin: AttractionHoursSoftPin,
         schedule_window: ItineraryScheduleWindow ) -> bool:
      return (
         soft_pin.open_seconds < schedule_window.end_seconds
         and soft_pin.close_seconds > schedule_window.start_seconds
      )


   @classmethod
   def _loop_id_by_attraction_name(
         cls,
         loop_units: list[ LoopScheduleUnit ],
      ) -> dict[ str, str ]:
      loop_ids: dict[ str, str ] = {}

      for loop_unit in loop_units:
         if loop_unit.loop_id is None:
            continue

         for stop in loop_unit.stops:
            if not isinstance(
                  stop,
                  ( ItineraryAttractionRecord, ItineraryTransportationRecord ) ):
               continue

            loop_ids[ stop.attraction ] = loop_unit.loop_id

      return loop_ids
