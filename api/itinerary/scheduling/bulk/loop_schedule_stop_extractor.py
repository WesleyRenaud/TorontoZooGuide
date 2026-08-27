from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from .loop_schedule_stop import LoopScheduleStop
from ....walk_graph.domain.master_route_stop_key import MasterRouteStopKey


class LoopScheduleStopExtractor():
   @classmethod
   def stop_key( cls, stop: LoopScheduleStop ) -> MasterRouteStopKey:
      return stop.master_route_stop_key()


   @classmethod
   def animals_from(
         cls,
         stops: list[ LoopScheduleStop ] ) -> list[ ItineraryAnimalRecord ]:
      return [
         stop
         for stop in stops
         if isinstance( stop, ItineraryAnimalRecord )
      ]


   @classmethod
   def attractions_from(
         cls,
         stops: list[ LoopScheduleStop ] ) -> list[ ItineraryAttractionRecord ]:
      return [
         stop
         for stop in stops
         if isinstance( stop, ItineraryAttractionRecord )
      ]


   @classmethod
   def transportations_from(
         cls,
         stops: list[ LoopScheduleStop ] ) -> list[ ItineraryTransportationRecord ]:
      return [
         stop
         for stop in stops
         if isinstance( stop, ItineraryTransportationRecord )
      ]
