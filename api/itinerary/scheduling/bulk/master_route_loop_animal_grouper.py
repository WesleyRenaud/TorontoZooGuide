from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from .master_route_loop_stop_grouper import MasterRouteLoopStopGrouper


class MasterRouteLoopAnimalGrouper():
   @classmethod
   def group(
         cls,
         animal_rows: list[ ItineraryAnimalRecord ] ) -> list[ list[ ItineraryAnimalRecord ] ]:
      return MasterRouteLoopStopGrouper.group( animal_rows )
