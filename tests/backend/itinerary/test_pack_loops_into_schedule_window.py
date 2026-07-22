from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from api.itinerary.scheduling.bulk.group_animals_by_master_route_loop import group_animals_by_master_route_loop
from api.itinerary.scheduling.bulk.loop_schedule_stop import LoopScheduleStop
from api.itinerary.scheduling.bulk.loop_schedule_unit import build_loop_schedule_units
from api.itinerary.scheduling.bulk.pack_loops_into_schedule_window import pack_loops_into_schedule_window
from api.itinerary.scheduling.bulk.pack_loops_into_schedule_window import PreparedLoopScheduleUnit
from api.shared.calendar_dates import DateValues
from api.shared.enums import ScheduleItemKind
from api.walk_graph.data_access.load_walk_graph import load_walk_graph


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


def _prepared_loop_unit(
      *,
      stops: list[ LoopScheduleStop ],
      duration_seconds: int ) -> PreparedLoopScheduleUnit:
   loop_unit = build_loop_schedule_units( [ stops ] )[ 0 ]

   return PreparedLoopScheduleUnit(
      unit=loop_unit,
      duration_seconds=duration_seconds,
   )


def _africa_meeting_spot_anchor_stop() -> ItineraryStop:
   return ItineraryStop(
      schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
      item_key='Masai Giraffe',
      walk_node_ids=( 'v-0304', ),
      meeting_spot='Wild Encounter - Africa Meeting Spot',
      is_fixed_time=True,
      start_time='11:00 AM',
      end_time='11:45 AM',
   )


def test_pack_loops_into_schedule_window_places_south_terminal_before_africa_anchor() -> None:
   walk_graph = load_walk_graph()
   window_start_seconds = DateValues.time_value_in_seconds( '9:00 AM' )
   window_end_seconds = DateValues.time_value_in_seconds( '11:00 AM' )

   assert window_start_seconds is not None
   assert window_end_seconds is not None

   australasia_unit = _prepared_loop_unit(
      stops=[
         _animal_record(
            species='Kookaburra',
            exhibit='Australasia Pavilion',
            enclosure_name='Indoor',
         ),
      ],
      duration_seconds=120,
   )
   indo_unit = _prepared_loop_unit(
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      duration_seconds=300,
   )

   packed_units = pack_loops_into_schedule_window(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds,
         anchor_stop=_africa_meeting_spot_anchor_stop(),
      ),
      prepared_units=[ australasia_unit, indo_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=str( walk_graph[ 'entrance_node_id' ] ),
   )

   assert [ unit.unit.loop_id for unit in packed_units ] == [
      'australasia',
      'indo_malaya',
   ]


def test_pack_loops_into_schedule_window_uses_open_window_greedy_order_without_anchor() -> None:
   walk_graph = load_walk_graph()
   window_start_seconds = DateValues.time_value_in_seconds( '9:00 AM' )
   window_end_seconds = DateValues.time_value_in_seconds( '12:00 PM' )

   assert window_start_seconds is not None
   assert window_end_seconds is not None

   australasia_unit = _prepared_loop_unit(
      stops=[
         _animal_record(
            species='Kookaburra',
            exhibit='Australasia Pavilion',
            enclosure_name='Indoor',
         ),
      ],
      duration_seconds=120,
   )
   indo_unit = _prepared_loop_unit(
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      duration_seconds=300,
   )

   packed_units = pack_loops_into_schedule_window(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds,
      ),
      prepared_units=[ australasia_unit, indo_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=str( walk_graph[ 'entrance_node_id' ] ),
   )

   assert [ unit.unit.loop_id for unit in packed_units ] == [
      'indo_malaya',
      'australasia',
   ]


def test_pack_loops_into_schedule_window_fits_partial_sequence_before_short_anchored_window() -> None:
   walk_graph = load_walk_graph()
   window_start_seconds = DateValues.time_value_in_seconds( '9:00 AM' )
   window_end_seconds = DateValues.time_value_in_seconds( '9:06 AM' )

   assert window_start_seconds is not None
   assert window_end_seconds is not None

   australasia_unit = _prepared_loop_unit(
      stops=[
         _animal_record(
            species='Kookaburra',
            exhibit='Australasia Pavilion',
            enclosure_name='Indoor',
         ),
      ],
      duration_seconds=120,
   )
   indo_unit = _prepared_loop_unit(
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      duration_seconds=300,
   )

   packed_units = pack_loops_into_schedule_window(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds,
         anchor_stop=_africa_meeting_spot_anchor_stop(),
      ),
      prepared_units=[ australasia_unit, indo_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=str( walk_graph[ 'entrance_node_id' ] ),
   )

   assert [ unit.unit.loop_id for unit in packed_units ] == [ 'indo_malaya' ]


def test_pack_loops_into_schedule_window_uses_itinerary_animal_nodes_for_partial_loop_endpoints() -> None:
   loop_units = build_loop_schedule_units(
      group_animals_by_master_route_loop(
         [
            _animal_record(
               species='Amur Tiger',
               exhibit='Eurasia Wilds',
            ),
            _animal_record(
               species='Capybara',
               exhibit='Americas Outdoor Mayan Temple Ruins',
            ),
         ],
      ),
   )
   loop_units_by_id = {
      loop_unit.loop_id: loop_unit
      for loop_unit in loop_units
   }

   assert loop_units_by_id[ 'australasia' ].entry_walk_node_id == 'v-1061'
   assert loop_units_by_id[ 'australasia' ].exit_walk_node_id == 'v-1061'
   assert loop_units_by_id[ 'tundra_trek_mayan_temple' ].entry_walk_node_id == 'v-0851'
   assert loop_units_by_id[ 'tundra_trek_mayan_temple' ].exit_walk_node_id == 'v-0851'


def test_pack_loops_into_schedule_window_orders_temple_before_eurasia_and_tiger_after_americas() -> None:
   walk_graph = load_walk_graph()
   window_start_seconds = DateValues.time_value_in_seconds( '2:00 PM' )
   window_end_seconds = DateValues.time_value_in_seconds( '5:00 PM' )

   assert window_start_seconds is not None
   assert window_end_seconds is not None

   prepared_units = [
      _prepared_loop_unit(
         stops=[
            _animal_record(
               species='Golden Lion Tamarin',
               exhibit='Americas Pavilion',
               enclosure_name='Outdoor',
            ),
         ],
         duration_seconds=600,
      ),
      _prepared_loop_unit(
         stops=[ _animal_record( species='Highland Cattle', exhibit='Eurasia Wilds' ) ],
         duration_seconds=600,
      ),
      _prepared_loop_unit(
         stops=[ _animal_record( species='Amur Tiger', exhibit='Eurasia Wilds' ) ],
         duration_seconds=300,
      ),
      _prepared_loop_unit(
         stops=[
            _animal_record(
               species='Capybara',
               exhibit='Americas Outdoor Mayan Temple Ruins',
            ),
         ],
         duration_seconds=600,
      ),
   ]

   packed_units = pack_loops_into_schedule_window(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds,
      ),
      prepared_units=prepared_units,
      cursor_seconds=window_start_seconds,
      current_node_id=str( walk_graph[ 'entrance_node_id' ] ),
   )

   assert [ unit.unit.loop_id for unit in packed_units ] == [
      'americas_pavilion',
      'tundra_trek_mayan_temple',
      'eurasia',
      'australasia',
   ]


def test_pack_loops_into_schedule_window_orients_two_way_loop_for_shorter_approach() -> None:
   walk_graph = load_walk_graph()
   window_start_seconds = DateValues.time_value_in_seconds( '2:00 PM' )
   window_end_seconds = DateValues.time_value_in_seconds( '5:00 PM' )

   assert window_start_seconds is not None
   assert window_end_seconds is not None

   temple_unit = _prepared_loop_unit(
      stops=[
         _animal_record(
            species='Capybara',
            exhibit='Americas Outdoor Mayan Temple Ruins',
         ),
      ],
      duration_seconds=600,
   )
   eurasia_unit = _prepared_loop_unit(
      stops=[
         _animal_record(
            species='Highland Cattle',
            exhibit='Eurasia Wilds',
         ),
         _animal_record(
            species='West Caucasian Tur',
            exhibit='Eurasia Wilds',
         ),
      ],
      duration_seconds=600,
   )

   packed_units = pack_loops_into_schedule_window(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds,
      ),
      prepared_units=[ eurasia_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=temple_unit.unit.exit_walk_node_id or '',
      departure_side_cluster_id='north',
   )

   assert len( packed_units ) == 1
   assert packed_units[ 0 ].unit.loop_id == 'eurasia'
   assert packed_units[ 0 ].unit.entry_walk_node_id == 'v-0955'
   assert packed_units[ 0 ].unit.exit_walk_node_id == 'v-1018'
   assert [ animal.species for animal in packed_units[ 0 ].unit.stops ] == [
      'West Caucasian Tur',
      'Highland Cattle',
   ]
