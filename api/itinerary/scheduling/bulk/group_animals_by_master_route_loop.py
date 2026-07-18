from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from .group_stops_by_master_route_loop import group_stops_by_master_route_loop


def group_animals_by_master_route_loop(
      animal_rows: list[ ItineraryAnimalRecord ] ) -> list[ list[ ItineraryAnimalRecord ] ]:
   return group_stops_by_master_route_loop( animal_rows )
