from __future__ import annotations

from dataclasses import dataclass

from ....animals.search.animals_matching_query import viewing_spot_key_from_values
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ....walk_graph.domain.master_route_loop import MasterRouteLoop
from ....walk_graph.master_route import default_loop_id_by_viewing_spot_key
from ....walk_graph.master_route import default_loop_index_in_side_cluster_by_loop_id
from ....walk_graph.master_route import default_loop_side_cluster_id_by_loop_id
from ....walk_graph.master_route import default_master_route_loop_by_id
from ....walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot


@dataclass( frozen=True )
class LoopScheduleUnit:
   loop_id: str | None
   animals: tuple[ ItineraryAnimalRecord, ... ]
   entry_walk_node_id: str | None
   exit_walk_node_id: str | None
   side_cluster_id: str | None
   loop_index_in_side_cluster: int | None


def build_loop_schedule_units(
      loop_groups: list[ list[ ItineraryAnimalRecord ] ] ) -> list[ LoopScheduleUnit ]:
   loop_ids_by_viewing_spot_key = default_loop_id_by_viewing_spot_key()
   loop_side_cluster_ids = default_loop_side_cluster_id_by_loop_id()
   loop_indexes_in_side_cluster = default_loop_index_in_side_cluster_by_loop_id()
   loops_by_id = default_master_route_loop_by_id()

   return [
      _loop_schedule_unit_from_group(
         animals,
         loop_ids_by_viewing_spot_key=loop_ids_by_viewing_spot_key,
         loop_side_cluster_ids=loop_side_cluster_ids,
         loop_indexes_in_side_cluster=loop_indexes_in_side_cluster,
         loops_by_id=loops_by_id )
      for animals in loop_groups
      if animals
   ]


def _loop_schedule_unit_from_group(
      animals: list[ ItineraryAnimalRecord ],
      *,
      loop_ids_by_viewing_spot_key: dict,
      loop_side_cluster_ids: dict[ str, str ],
      loop_indexes_in_side_cluster: dict[ str, int ],
      loops_by_id: dict ) -> LoopScheduleUnit:
   loop_id = _loop_id_for_animals( animals, loop_ids_by_viewing_spot_key )

   if loop_id is None:
      return _unmapped_loop_schedule_unit( animals )

   master_route_loop = loops_by_id[ loop_id ]
   entry_walk_node_id, exit_walk_node_id = _loop_walk_endpoint_node_ids_for_animals(
      master_route_loop,
      animals )

   return LoopScheduleUnit(
      loop_id=loop_id,
      animals=tuple( animals ),
      entry_walk_node_id=entry_walk_node_id,
      exit_walk_node_id=exit_walk_node_id,
      side_cluster_id=loop_side_cluster_ids.get( loop_id ),
      loop_index_in_side_cluster=loop_indexes_in_side_cluster.get( loop_id ),
   )


def _loop_walk_endpoint_node_ids_for_animals(
      master_route_loop: MasterRouteLoop,
      animals: list[ ItineraryAnimalRecord ] ) -> tuple[ str | None, str | None ]:
   animals_in_loop_order = _animals_in_master_route_loop_order(
      master_route_loop,
      animals )

   if not animals_in_loop_order:
      return None, None

   first_animal = animals_in_loop_order[ 0 ]
   last_animal = animals_in_loop_order[ -1 ]

   return (
      _walk_node_id_for_animal( first_animal ),
      _walk_node_id_for_animal( last_animal ),
   )


def _animals_in_master_route_loop_order(
      master_route_loop: MasterRouteLoop,
      animals: list[ ItineraryAnimalRecord ] ) -> list[ ItineraryAnimalRecord ]:
   loop_index_by_viewing_spot_key = {
      viewing_spot_key_from_values(
         viewing_spot.species,
         viewing_spot.exhibit,
         viewing_spot.name ): loop_index
      for loop_index, viewing_spot in enumerate( master_route_loop.viewing_spots )
   }
   animals_in_loop = [
      animal_row
      for animal_row in animals
      if animal_row.viewing_spot_key() in loop_index_by_viewing_spot_key
   ]

   if not animals_in_loop:
      return list( animals )

   animals_in_loop.sort(
      key=lambda animal_row: loop_index_by_viewing_spot_key[
         animal_row.viewing_spot_key() ] )

   return animals_in_loop


def _walk_node_id_for_animal(
      animal_row: ItineraryAnimalRecord ) -> str | None:
   return walk_node_id_for_viewing_spot(
      animal_row.species,
      animal_row.exhibit,
      animal_row.enclosure_name )


def _loop_id_for_animals(
      animals: list[ ItineraryAnimalRecord ],
      loop_ids_by_viewing_spot_key: dict ) -> str | None:
   for animal_row in animals:
      loop_id = loop_ids_by_viewing_spot_key.get( animal_row.viewing_spot_key() )

      if loop_id is not None:
         return loop_id

   return None


def _unmapped_loop_schedule_unit(
      animals: list[ ItineraryAnimalRecord ] ) -> LoopScheduleUnit:
   first_animal = animals[ 0 ]
   last_animal = animals[ -1 ]

   return LoopScheduleUnit(
      loop_id=None,
      animals=tuple( animals ),
      entry_walk_node_id=_walk_node_id_for_animal( first_animal ),
      exit_walk_node_id=_walk_node_id_for_animal( last_animal ),
      side_cluster_id=None,
      loop_index_in_side_cluster=None,
   )
