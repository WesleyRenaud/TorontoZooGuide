from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ....walk_graph.domain.walk_graph import WalkGraph
from ....walk_graph.enclosure_viewing_walk_node_lookup import walk_nodes_for_species_exhibit
from ....walk_graph.representative_walk_node import representative_walk_node_id_from_candidates
from ....walk_graph.shortest_path import build_walk_graph_adjacency
from ....walk_graph.shortest_path import shortest_path_distances


def representative_walk_node_id(
      graph: WalkGraph,
      from_node_id: str,
      species: str,
      exhibit: str ) -> str | None:
   return representative_walk_node_id_from_candidates(
      graph,
      from_node_id,
      _viewing_node_ids( species, exhibit ) )


def walk_travel_distance_px(
      graph: WalkGraph,
      from_node_id: str,
      species: str,
      exhibit: str ) -> float | None:
   viewing_node_ids = _viewing_node_ids( species, exhibit )
   distances = shortest_path_distances( graph, from_node_id )

   return _min_distance_to_viewing_nodes( distances, viewing_node_ids )


def sort_animals_for_bulk_schedule(
      graph: WalkGraph,
      animal_rows: list[ ItineraryAnimalRecord ],
      *,
      start_node_id: str ) -> list[ ItineraryAnimalRecord ]:
   if not animal_rows:
      return []

   adjacency = build_walk_graph_adjacency( graph )
   viewing_node_ids_by_animal = {
      ( animal_row.species, animal_row.exhibit ): _viewing_node_ids(
         animal_row.species,
         animal_row.exhibit )
      for animal_row in animal_rows
   }

   remaining_animals = list( animal_rows )
   ordered_animals: list[ ItineraryAnimalRecord ] = []
   current_node_id = start_node_id

   while remaining_animals:
      distances = shortest_path_distances(
         graph,
         current_node_id,
         adjacency=adjacency )

      next_animal = min(
         remaining_animals,
         key=lambda animal_row: _bulk_schedule_walk_sort_key_from_distances(
            distances,
            animal_row,
            viewing_node_ids_by_animal[
               ( animal_row.species, animal_row.exhibit ) ] ) )
      remaining_animals.remove( next_animal )
      ordered_animals.append( next_animal )

      next_node_id = representative_walk_node_id_from_candidates(
         graph,
         current_node_id,
         viewing_node_ids_by_animal[
            ( next_animal.species, next_animal.exhibit ) ] )

      if next_node_id is not None:
         current_node_id = next_node_id

   return ordered_animals


def _viewing_node_ids( species: str, exhibit: str ) -> tuple[ str, ... ]:
   return tuple(
      str( row[ 'walk_node_id' ] )
      for row in walk_nodes_for_species_exhibit( species, exhibit ) )


def _min_distance_to_viewing_nodes(
      distances: dict[ str, float ],
      viewing_node_ids: tuple[ str, ... ] ) -> float | None:
   shortest_distance_px: float | None = None

   for node_id in viewing_node_ids:
      distance_px = distances.get( node_id )

      if distance_px is None:
         continue

      if (
            shortest_distance_px is None
            or distance_px < shortest_distance_px ):
         shortest_distance_px = distance_px

   return shortest_distance_px


def _bulk_schedule_walk_sort_key_from_distances(
      distances: dict[ str, float ],
      animal_row: ItineraryAnimalRecord,
      viewing_node_ids: tuple[ str, ... ] ) -> tuple[ float, str, str ]:
   distance_px = _min_distance_to_viewing_nodes(
      distances,
      viewing_node_ids )

   if distance_px is None:
      return ( float( 'inf' ), animal_row.exhibit.lower(), animal_row.species.lower() )

   return ( distance_px, animal_row.exhibit.lower(), animal_row.species.lower() )
