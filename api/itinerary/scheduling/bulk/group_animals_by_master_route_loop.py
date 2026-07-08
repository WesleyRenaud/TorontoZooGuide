from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from .sort_animals_by_master_route import sort_animals_by_master_route
from ....walk_graph.master_route import default_loop_index_by_viewing_spot_key


def group_animals_by_master_route_loop(
      animal_rows: list[ ItineraryAnimalRecord ] ) -> list[ list[ ItineraryAnimalRecord ] ]:
   sorted_animals = sort_animals_by_master_route( animal_rows )

   if not sorted_animals:
      return []

   loop_indexes = default_loop_index_by_viewing_spot_key()
   groups: list[ list[ ItineraryAnimalRecord ] ] = []
   current_loop_index: int | None = None
   current_group: list[ ItineraryAnimalRecord ] = []

   for animal_row in sorted_animals:
      loop_index = loop_indexes.get( animal_row.viewing_spot_key() )

      if loop_index is None:
         if current_group:
            groups.append( current_group )
            current_group = []
            current_loop_index = None

         groups.append( [ animal_row ] )
         continue

      if loop_index != current_loop_index:
         if current_group:
            groups.append( current_group )

         current_group = [ animal_row ]
         current_loop_index = loop_index
         continue

      current_group.append( animal_row )

   if current_group:
      groups.append( current_group )

   return groups
