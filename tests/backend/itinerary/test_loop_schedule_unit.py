from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.group_animals_by_master_route_loop import group_animals_by_master_route_loop
from api.itinerary.scheduling.bulk.loop_schedule_unit import build_loop_schedule_units
from api.itinerary.scheduling.bulk.loop_schedule_unit import loop_schedule_unit_reversed


def _animal_record(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> ItineraryAnimalRecord:
   return ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      old_likelihood=None,
      new_likelihood=100,
   )


def test_build_loop_schedule_units_assigns_loop_id_side_cluster_and_walk_endpoints() -> None:
   loop_groups = group_animals_by_master_route_loop(
      [
         _animal_record(
            species='Kookaburra',
            exhibit='Australasia Pavilion',
            enclosure_name='Indoor',
         ),
         _animal_record(
            species='Cheetah',
            exhibit='Indo-Malaya Outdoor',
         ),
      ],
   )
   loop_units = build_loop_schedule_units( loop_groups )

   assert len( loop_units ) == 2

   australasia_unit = loop_units[ 0 ]
   indo_unit = loop_units[ 1 ]

   assert australasia_unit.loop_id == 'australasia'
   assert australasia_unit.side_cluster_id == 'north'
   assert australasia_unit.entry_walk_node_id == 'v-1139'
   assert australasia_unit.exit_walk_node_id == 'v-1139'
   assert [ animal.species for animal in australasia_unit.animals ] == [ 'Kookaburra' ]

   assert indo_unit.loop_id == 'indo_malaya'
   assert indo_unit.side_cluster_id == 'south'
   assert indo_unit.entry_walk_node_id == 'v-0226'
   assert indo_unit.exit_walk_node_id == 'v-0226'
   assert [ animal.species for animal in indo_unit.animals ] == [ 'Cheetah' ]


def test_build_loop_schedule_units_uses_itinerary_animals_for_partial_loop_endpoints() -> None:
   loop_units = build_loop_schedule_units(
      group_animals_by_master_route_loop(
         [
            _animal_record(
               species='Amur Tiger',
               exhibit='Eurasia Wilds',
            ),
         ],
      ),
   )

   assert len( loop_units ) == 1
   assert loop_units[ 0 ].loop_id == 'australasia'
   assert loop_units[ 0 ].entry_walk_node_id == 'v-1061'
   assert loop_units[ 0 ].exit_walk_node_id == 'v-1061'


def test_build_loop_schedule_units_store_two_way_traversal() -> None:
   loop_units = build_loop_schedule_units(
      group_animals_by_master_route_loop(
         [
            _animal_record(
               species='Highland Cattle',
               exhibit='Eurasia Wilds',
            ),
            _animal_record(
               species='West Caucasian Tur',
               exhibit='Eurasia Wilds',
            ),
         ],
      ),
   )

   assert len( loop_units ) == 1
   assert loop_units[ 0 ].traversal == 'two_way'
   assert loop_units[ 0 ].entry_walk_node_id == 'v-1018'
   assert loop_units[ 0 ].exit_walk_node_id == 'v-0955'


def test_loop_schedule_unit_reversed_swaps_endpoints_and_animals() -> None:
   loop_units = build_loop_schedule_units(
      group_animals_by_master_route_loop(
         [
            _animal_record(
               species='Highland Cattle',
               exhibit='Eurasia Wilds',
            ),
            _animal_record(
               species='West Caucasian Tur',
               exhibit='Eurasia Wilds',
            ),
         ],
      ),
   )
   reversed_unit = loop_schedule_unit_reversed( loop_units[ 0 ] )

   assert reversed_unit.entry_walk_node_id == 'v-0955'
   assert reversed_unit.exit_walk_node_id == 'v-1018'
   assert [ animal.species for animal in reversed_unit.animals ] == [
      'West Caucasian Tur',
      'Highland Cattle',
   ]


def test_build_loop_schedule_units_leaves_unmapped_animals_without_side_cluster() -> None:
   loop_units = build_loop_schedule_units(
      [
         [
            _animal_record(
               species='Unknown Animal',
               exhibit='Nowhere',
            ),
         ],
      ],
   )

   assert len( loop_units ) == 1
   assert loop_units[ 0 ].loop_id is None
   assert loop_units[ 0 ].side_cluster_id is None
