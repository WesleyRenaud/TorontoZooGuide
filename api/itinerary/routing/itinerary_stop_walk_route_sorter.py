from __future__ import annotations

from .itinerary_stop import ItineraryStop
from ...shared.calendar_dates import DateValues
from ...shared.enums import ScheduleItemKind


class ItineraryStopWalkRouteSorter():
   @classmethod
   def sort( cls, stops: list[ ItineraryStop ] ) -> list[ ItineraryStop ]:
      entrance_stop = next(
         (
            stop
            for stop in stops
            if stop.schedule_item_kind == ScheduleItemKind.ENTRANCE
         ),
         None )
      scheduled_stops = [
         stop
         for stop in stops
         if stop.is_fixed_time
         and stop.schedule_item_kind != ScheduleItemKind.ENTRANCE
      ]

      if not scheduled_stops:
         return []

      scheduled_stops.sort( key=cls._walk_route_stop_sort_key )

      if entrance_stop is None:
         return scheduled_stops

      return [ entrance_stop, *scheduled_stops ]


   @classmethod
   def _walk_route_stop_sort_key(
         cls,
         stop: ItineraryStop ) -> tuple[ int, str, str ]:
      start_seconds = DateValues.time_value_in_seconds( stop.start_time )

      return (
         start_seconds,
         stop.schedule_item_kind.value,
         stop.item_key.lower(),
      )
