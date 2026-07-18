from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from api.itinerary.scheduling.bulk.group_animals_by_master_route_loop import group_animals_by_master_route_loop
from api.itinerary.scheduling.bulk.loop_schedule_unit import build_loop_schedule_units
from api.itinerary.scheduling.bulk.pack_loops_into_schedule_window import pack_loops_into_schedule_window
from api.itinerary.scheduling.bulk.pack_loops_into_schedule_window import prepare_loop_schedule_units
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.shortest_path import shortest_path_distance
from conftest import DbControllers

GOLDEN_LION_TAMARIN_ITINERARY_ENTRY = {
   'species': 'Golden Lion Tamarin',
   'exhibit': 'Americas Pavilion',
   'enclosure_name': 'Outdoor',
}

CAPYBARA_TEMPLE_ITINERARY_ENTRY = {
   'species': 'Capybara',
   'exhibit': 'Americas Outdoor Mayan Temple Ruins',
}

HIGHLAND_CATTLE_ITINERARY_ENTRY = {
   'species': 'Highland Cattle',
   'exhibit': 'Eurasia Wilds',
}

WEST_CAUCASIAN_TUR_ITINERARY_ENTRY = {
   'species': 'West Caucasian Tur',
   'exhibit': 'Eurasia Wilds',
}

AMERICAS_PAVILION_TO_EURASIA_ITINERARY = [
   GOLDEN_LION_TAMARIN_ITINERARY_ENTRY,
   CAPYBARA_TEMPLE_ITINERARY_ENTRY,
   HIGHLAND_CATTLE_ITINERARY_ENTRY,
   WEST_CAUCASIAN_TUR_ITINERARY_ENTRY,
]


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


def test_bulk_schedule_animals_reverses_eurasia_loop_after_temple_for_shorter_walk(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=AMERICAS_PAVILION_TO_EURASIA_ITINERARY,
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == []

   tamarin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Golden Lion Tamarin' )
   capybara = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Capybara' )
   cattle = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Highland Cattle' )
   tur = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'West Caucasian Tur' )

   tamarin_end_seconds = DateValues.time_value_in_seconds( tamarin.end_time )
   capybara_start_seconds = DateValues.time_value_in_seconds( capybara.start_time )
   capybara_end_seconds = DateValues.time_value_in_seconds( capybara.end_time )
   tur_start_seconds = DateValues.time_value_in_seconds( tur.start_time )
   tur_end_seconds = DateValues.time_value_in_seconds( tur.end_time )
   cattle_start_seconds = DateValues.time_value_in_seconds( cattle.start_time )

   assert tamarin_end_seconds is not None
   assert capybara_start_seconds is not None
   assert capybara_end_seconds is not None
   assert tur_start_seconds is not None
   assert tur_end_seconds is not None
   assert cattle_start_seconds is not None

   assert tamarin_end_seconds <= capybara_start_seconds
   assert capybara_end_seconds <= tur_start_seconds
   assert tur_end_seconds <= cattle_start_seconds
   assert tur_start_seconds < cattle_start_seconds


def test_packing_americas_pavilion_to_eurasia_itinerary_saves_walk_after_temple(
      db: DbControllers ) -> None:
   assert db.conn is not None

   walk_graph = load_walk_graph()
   window_start_seconds = DateValues.time_value_in_seconds( '9:00 AM' )
   window_end_seconds = DateValues.time_value_in_seconds( '5:00 PM' )

   assert window_start_seconds is not None
   assert window_end_seconds is not None

   animal_rows = [
      _animal_record(
         species=entry[ 'species' ],
         exhibit=entry[ 'exhibit' ],
         enclosure_name=entry.get( 'enclosure_name' ),
      )
      for entry in AMERICAS_PAVILION_TO_EURASIA_ITINERARY
   ]
   prepared_units = prepare_loop_schedule_units(
      db.conn,
      build_loop_schedule_units(
         group_animals_by_master_route_loop( animal_rows ) ) )

   assert prepared_units is not None

   prepared_units_by_loop_id = {
      prepared_unit.unit.loop_id: prepared_unit
      for prepared_unit in prepared_units
   }
   americas_exit = (
      prepared_units_by_loop_id[ 'americas_pavilion' ].unit.exit_walk_node_id )
   temple_unit = prepared_units_by_loop_id[ 'tundra_trek_mayan_temple' ]
   eurasia_unit = prepared_units_by_loop_id[ 'eurasia' ]

   assert americas_exit is not None

   packed_units = pack_loops_into_schedule_window(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds,
      ),
      prepared_units=[ temple_unit, eurasia_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=americas_exit,
      departure_side_cluster_id='north',
   )

   assert [ unit.unit.loop_id for unit in packed_units ] == [
      'tundra_trek_mayan_temple',
      'eurasia',
   ]
   assert [ animal.species for animal in packed_units[ 1 ].unit.animals ] == [
      'West Caucasian Tur',
      'Highland Cattle',
   ]

   temple_exit = packed_units[ 0 ].unit.exit_walk_node_id
   eurasia_forward_entry = eurasia_unit.unit.entry_walk_node_id
   eurasia_reverse_entry = eurasia_unit.unit.exit_walk_node_id

   assert temple_exit is not None
   assert eurasia_forward_entry is not None
   assert eurasia_reverse_entry is not None

   oriented_approach_distance = shortest_path_distance(
      walk_graph,
      temple_exit,
      packed_units[ 1 ].unit.entry_walk_node_id )
   forward_only_approach_distance = shortest_path_distance(
      walk_graph,
      temple_exit,
      eurasia_forward_entry )

   assert oriented_approach_distance is not None
   assert forward_only_approach_distance is not None
   assert oriented_approach_distance < forward_only_approach_distance
   assert forward_only_approach_distance - oriented_approach_distance > 500
