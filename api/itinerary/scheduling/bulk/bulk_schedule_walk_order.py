from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ....walk_graph.domain.walk_graph import WalkGraph
from ....walk_graph.enclosure_viewing_walk_node_lookup import walk_nodes_for_species_exhibit
from ....walk_graph.shortest_path import shortest_path_distance


def representative_walk_node_id(
      graph: WalkGraph,
      from_node_id: str,
      species: str,
      exhibit: str ) -> str | None:
   walk_node_id: str | None = None
   shortest_distance_px: float | None = None

   for row in walk_nodes_for_species_exhibit( species, exhibit ):
      distance_px = shortest_path_distance(
         graph,
         from_node_id,
         row[ 'walk_node_id' ] )

      if distance_px is None:
         continue

      if (
            shortest_distance_px is None
            or distance_px < shortest_distance_px ):
         shortest_distance_px = distance_px
         walk_node_id = row[ 'walk_node_id' ]

   return walk_node_id


def walk_travel_distance_px(
      graph: WalkGraph,
      from_node_id: str,
      species: str,
      exhibit: str ) -> float | None:
   target_node_id = representative_walk_node_id(
      graph,
      from_node_id,
      species,
      exhibit )

   if target_node_id is None:
      return None

   return shortest_path_distance( graph, from_node_id, target_node_id )


def sort_animals_for_bulk_schedule(
      graph: WalkGraph,
      animal_rows: list[ ItineraryAnimalRecord ],
      *,
      start_node_id: str ) -> list[ ItineraryAnimalRecord ]:
   remaining_animals = list( animal_rows )
   ordered_animals: list[ ItineraryAnimalRecord ] = []
   current_node_id = start_node_id

   while remaining_animals:
      next_animal = min(
         remaining_animals,
         key=lambda animal_row: _bulk_schedule_walk_sort_key(
            graph,
            current_node_id,
            animal_row ) )
      remaining_animals.remove( next_animal )
      ordered_animals.append( next_animal )

      next_node_id = representative_walk_node_id(
         graph,
         current_node_id,
         next_animal.species,
         next_animal.exhibit )

      if next_node_id is not None:
         current_node_id = next_node_id

   return ordered_animals


def _bulk_schedule_walk_sort_key(
      graph: WalkGraph,
      from_node_id: str,
      animal_row: ItineraryAnimalRecord ) -> tuple[ float, str, str ]:
   distance_px = walk_travel_distance_px(
      graph,
      from_node_id,
      animal_row.species,
      animal_row.exhibit )

   if distance_px is None:
      return ( float( 'inf' ), animal_row.exhibit.lower(), animal_row.species.lower() )

   return ( distance_px, animal_row.exhibit.lower(), animal_row.species.lower() )
