from __future__ import annotations

from dataclasses import dataclass

from .itinerary_stop import ItineraryStop
from ..scheduling.core.time_block import time_block_from_schedule_times


@dataclass( frozen=True )
class ItineraryFixedTimeStop:
   stop: ItineraryStop
   start_seconds: int
   end_seconds: int


def itinerary_fixed_time_stops_from_itinerary_stops(
      itinerary_stops: list[ ItineraryStop ] ) -> list[ ItineraryFixedTimeStop ]:
   fixed_time_stops: list[ ItineraryFixedTimeStop ] = []

   for itinerary_stop in itinerary_stops:
      fixed_time_stop = itinerary_fixed_time_stop_from_itinerary_stop(
         itinerary_stop )

      if fixed_time_stop is not None:
         fixed_time_stops.append( fixed_time_stop )

   return fixed_time_stops


def itinerary_fixed_time_stop_from_itinerary_stop(
      itinerary_stop: ItineraryStop ) -> ItineraryFixedTimeStop | None:
   time_block = time_block_from_schedule_times(
      itinerary_stop.start_time,
      itinerary_stop.end_time )

   if time_block is None:
      return None

   return ItineraryFixedTimeStop(
      stop=itinerary_stop,
      start_seconds=time_block.start_seconds,
      end_seconds=time_block.end_seconds )
