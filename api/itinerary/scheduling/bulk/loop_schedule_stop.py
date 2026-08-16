from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ....walk_graph.domain.master_route_stop_key import MasterRouteStopKey


LoopScheduleStop = (
   ItineraryAnimalRecord
   | ItineraryAttractionRecord
   | ItineraryTransportationRecord
)


def loop_schedule_stop_key( stop: LoopScheduleStop ) -> MasterRouteStopKey:
   return stop.master_route_stop_key()


def animals_from_stops(
      stops: list[ LoopScheduleStop ] ) -> list[ ItineraryAnimalRecord ]:
   return [
      stop
      for stop in stops
      if isinstance( stop, ItineraryAnimalRecord )
   ]


def attractions_from_stops(
      stops: list[ LoopScheduleStop ] ) -> list[ ItineraryAttractionRecord ]:
   return [
      stop
      for stop in stops
      if isinstance( stop, ItineraryAttractionRecord )
   ]


def transportations_from_stops(
      stops: list[ LoopScheduleStop ] ) -> list[ ItineraryTransportationRecord ]:
   return [
      stop
      for stop in stops
      if isinstance( stop, ItineraryTransportationRecord )
   ]
