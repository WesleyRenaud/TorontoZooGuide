from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ....walk_graph.master_route import default_master_route_index_by_viewing_spot_key


def sort_animals_by_master_route(
      animal_rows: list[ ItineraryAnimalRecord ] ) -> list[ ItineraryAnimalRecord ]:
   if not animal_rows:
      return []

   master_route_indexes = default_master_route_index_by_viewing_spot_key()
   mapped_animals: list[ ItineraryAnimalRecord ] = []
   unmapped_animals: list[ ItineraryAnimalRecord ] = []

   for animal_row in animal_rows:
      if animal_row.viewing_spot_key() in master_route_indexes:
         mapped_animals.append( animal_row )
      else:
         unmapped_animals.append( animal_row )

   mapped_animals.sort(
      key=lambda animal_row: master_route_indexes[
         animal_row.viewing_spot_key() ] )
   unmapped_animals.sort( key=_unmapped_animal_sort_key )

   return mapped_animals + unmapped_animals


def _unmapped_animal_sort_key(
      animal_row: ItineraryAnimalRecord ) -> tuple[ str, str, str ]:
   return (
      animal_row.exhibit.lower(),
      ( animal_row.enclosure_name or '' ).lower(),
      animal_row.species.lower(),
   )
