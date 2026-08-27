from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CAROUSEL, CHEETAH_INDO_MALAYA_ITINERARY_ENTRY, entrance_travel_seconds_to_animal, LION_ITINERARY_ENTRY, LION_KEY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, schedule_itinerary_item, schedule_time_after_seconds, unschedule_itinerary_item

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from api.itinerary.routing.transportation_walk_node_resolver import TransportationWalkNodeResolver
from api.itinerary.routing.walk_travel_time_calculator import WALK_PX_PER_MINUTE
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_schedule_slot_assigner import LoopScheduleSlotAssigner
from api.itinerary.scheduling.bulk.loop_schedule_unit_builder import LoopScheduleUnitBuilder
from api.itinerary.scheduling.bulk.loop_unit_travel_time_calculator import LoopUnitTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_window_packer import LoopWindowPacker
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.itinerary.scheduling.bulk.timed_loop_schedule_stop import TimedLoopScheduleStop
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.map_location_walk_node_lookup import walk_node_for_map_location
from api.walk_graph.shortest_path import shortest_path
from api.walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot
from conftest import DbControllers

ZOOMOBILE = 'Zoomobile'

LION_TRAVEL_SECONDS = entrance_travel_seconds_to_animal(
   species='African Lion',
   exhibit='Africa Savanna',
)
CHEETAH_INDO_TRAVEL_SECONDS = entrance_travel_seconds_to_animal(
   species='Cheetah',
   exhibit='Indo-Malaya Outdoor',
)
PENGUIN_TRAVEL_SECONDS = entrance_travel_seconds_to_animal(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)
GRIZZLY_ITINERARY_ENTRY = {
   'species': 'Grizzly Bear',
   'exhibit': 'Canadian Domain',
}
GRIZZLY_KEY = 'Grizzly Bear||Canadian Domain'
GRIZZLY_WALK_NODE_ID = 'v-0623'


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


def _timed_stop(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None,
      duration_seconds: int = 0,
      travel_before_seconds: int = 0 ) -> TimedLoopScheduleStop:
   return TimedLoopScheduleStop(
      stop=_animal_record(
         species=species,
         exhibit=exhibit,
         enclosure_name=enclosure_name ),
      duration_seconds=duration_seconds,
      travel_before_seconds=travel_before_seconds,
   )


def _prepared_loop_unit(
      *,
      stops: list[ ItineraryAnimalRecord ],
      duration_seconds: int ) -> PreparedLoopScheduleUnit:
   return PreparedLoopScheduleUnit(
      unit=LoopScheduleUnitBuilder.build( [ stops ] )[ 0 ],
      occupied_seconds=duration_seconds,
   )


def _travel_seconds_between_animals(
      *,
      from_species: str,
      from_exhibit: str,
      to_species: str,
      to_exhibit: str,
      from_enclosure_name: str | None = None,
      to_enclosure_name: str | None = None ) -> int:
   walk_graph = load_walk_graph()
   from_node_id = walk_node_id_for_viewing_spot(
      from_species,
      from_exhibit,
      from_enclosure_name )
   to_node_id = walk_node_id_for_viewing_spot(
      to_species,
      to_exhibit,
      to_enclosure_name )
   assert from_node_id is not None
   assert to_node_id is not None

   return WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      from_node_id,
      to_node_id )


def _seconds( schedule_time: str | None ) -> int:
   value = DateValues.time_value_in_seconds( schedule_time )
   assert value is not None

   return value


# --- Helper unit tests -------------------------------------------------------


def test_travel_time_seconds_from_length_px_uses_floored_minutes() -> None:
   assert WalkTravelTimeCalculator.seconds_from_length_px( 0 ) == 0
   assert WalkTravelTimeCalculator.seconds_from_length_px( 0.5 * WALK_PX_PER_MINUTE ) == 0
   assert WalkTravelTimeCalculator.seconds_from_length_px( 1.0 * WALK_PX_PER_MINUTE ) == 60
   assert WalkTravelTimeCalculator.seconds_from_length_px( 1.5 * WALK_PX_PER_MINUTE ) == 60
   assert WalkTravelTimeCalculator.seconds_from_length_px( 2.9 * WALK_PX_PER_MINUTE ) == 120


def test_travel_time_seconds_between_identical_nodes_is_zero() -> None:
   walk_graph = load_walk_graph()
   lion_node_id = walk_node_id_for_viewing_spot(
      'African Lion',
      'Africa Savanna',
      None )
   assert lion_node_id is not None
   assert WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      lion_node_id,
      lion_node_id ) == 0


def test_travel_time_seconds_between_nodes_matches_floor_helper() -> None:
   walk_graph = load_walk_graph()
   path = shortest_path(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      GRIZZLY_WALK_NODE_ID )
   assert path is not None
   assert WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      GRIZZLY_WALK_NODE_ID ) == WalkTravelTimeCalculator.seconds_from_length_px( path.length_px )
   assert WalkTravelTimeCalculator.seconds_for_shortest_path( path ) == (
      WalkTravelTimeCalculator.minutes_from_length_px( path.length_px ) * 60 )
   assert WalkTravelTimeCalculator.seconds_for_shortest_path( None ) == 0


def test_travel_time_seconds_between_unreachable_nodes_is_zero() -> None:
   walk_graph = load_walk_graph()
   assert WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      'not-a-real-node' ) == 0


# --- Contiguous slot packing -------------------------------------------------


def test_assign_contiguous_slots_inserts_inter_stop_travel_gaps() -> None:
   stops = [
      _timed_stop(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         duration_seconds=300,
         travel_before_seconds=0 ),
      _timed_stop(
         species='African Lion',
         exhibit='Africa Savanna',
         duration_seconds=480,
         travel_before_seconds=540 ),
   ]
   start_seconds = _seconds( '9:30 AM' )
   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous(
      stops,
      start_seconds=start_seconds )

   assert [ slot[ 1 ] for slot in slots ] == [ '9:30 AM', '9:44 AM' ]
   assert [ slot[ 2 ] for slot in slots ] == [ '9:35 AM', '9:52 AM' ]
   assert end_seconds == start_seconds + 300 + 540 + 480


def test_assign_contiguous_slots_without_travel_stays_flush() -> None:
   stops = [
      _timed_stop(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         duration_seconds=300,
         travel_before_seconds=0 ),
      _timed_stop(
         species='African Lion',
         exhibit='Africa Savanna',
         duration_seconds=480,
         travel_before_seconds=0 ),
   ]
   start_seconds = _seconds( '9:30 AM' )
   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous(
      stops,
      start_seconds=start_seconds )

   assert [ slot[ 1 ] for slot in slots ] == [ '9:30 AM', '9:35 AM' ]
   assert end_seconds == start_seconds + 300 + 480


def test_assign_contiguous_slots_zero_travel_keeps_flush_behavior() -> None:
   stops = [
      _timed_stop(
         species='African Lion',
         exhibit='Africa Savanna',
         duration_seconds=480,
         travel_before_seconds=0 ),
      _timed_stop(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
         duration_seconds=420,
         travel_before_seconds=0 ),
   ]
   start_seconds = _seconds( '10:00 AM' )
   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous(
      stops,
      start_seconds=start_seconds )

   assert slots[ 1 ][ 1 ] == '10:08 AM'
   assert end_seconds == start_seconds + 480 + 420


def test_assign_contiguous_slots_ending_by_reserves_travel_before_deadline() -> None:
   stops = [
      _timed_stop(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         duration_seconds=300,
         travel_before_seconds=0 ),
      _timed_stop(
         species='African Lion',
         exhibit='Africa Savanna',
         duration_seconds=480,
         travel_before_seconds=540 ),
   ]
   deadline_seconds = _seconds( '11:00 AM' )
   assignment = LoopScheduleSlotAssigner.assign_contiguous_ending_by(
      stops,
      end_seconds=deadline_seconds )

   assert assignment is not None
   slots, end_seconds = assignment
   assert end_seconds == deadline_seconds
   assert slots[ 0 ][ 1 ] == '10:38 AM'
   assert slots[ 1 ][ 1 ] == '10:52 AM'


# --- Loop unit travel helpers ------------------------------------------------


def test_approach_travel_seconds_to_unit_is_zero_from_entry_node() -> None:
   walk_graph = load_walk_graph()
   unit = LoopScheduleUnitBuilder.build(
      [
         [
            _animal_record(
               species='Cheetah',
               exhibit='Indo-Malaya Outdoor' ),
         ],
      ] )[ 0 ]
   assert unit.entry_walk_node_id is not None
   assert LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
      walk_graph,
      unit.entry_walk_node_id,
      unit ) == 0


def test_approach_travel_seconds_to_unit_from_entrance_matches_helper() -> None:
   walk_graph = load_walk_graph()
   unit = LoopScheduleUnitBuilder.build(
      [
         [
            _animal_record(
               species='Cheetah',
               exhibit='Indo-Malaya Outdoor' ),
         ],
      ] )[ 0 ]
   assert LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
      walk_graph,
      str( walk_graph[ 'entrance_node_id' ] ),
      unit ) == CHEETAH_INDO_TRAVEL_SECONDS


def test_inter_stop_travel_seconds_between_two_animals() -> None:
   walk_graph = load_walk_graph()
   stops = [
      _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ),
      _animal_record( species='African Lion', exhibit='Africa Savanna' ),
   ]
   travels = LoopUnitTravelTimeCalculator.inter_stop_seconds( walk_graph, stops )
   expected = _travel_seconds_between_animals(
      from_species='Cheetah',
      from_exhibit='Indo-Malaya Outdoor',
      to_species='African Lion',
      to_exhibit='Africa Savanna' )

   assert travels == [ 0, expected ]
   assert LoopUnitTravelTimeCalculator.total_inter_stop_seconds( walk_graph, stops ) == expected
   assert LoopUnitTravelTimeCalculator.inter_stop_seconds( walk_graph, stops[ :1 ] ) == [ 0 ]


def test_packed_units_occupied_seconds_includes_approach_and_duration() -> None:
   walk_graph = load_walk_graph()
   entrance_node_id = str( walk_graph[ 'entrance_node_id' ] )
   indo_unit = _prepared_loop_unit(
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      duration_seconds=300 )
   africa_unit = _prepared_loop_unit(
      stops=[ _animal_record( species='African Lion', exhibit='Africa Savanna' ) ],
      duration_seconds=480 )

   occupied = LoopUnitTravelTimeCalculator.packed_units_occupied_seconds(
      walk_graph,
      [ indo_unit, africa_unit ],
      from_node_id=entrance_node_id )
   first_approach = LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
      walk_graph,
      entrance_node_id,
      indo_unit.unit )
   second_approach = LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
      walk_graph,
      indo_unit.unit.exit_walk_node_id or entrance_node_id,
      africa_unit.unit )

   assert occupied == first_approach + 300 + second_approach + 480
   assert occupied > 300 + 480


# --- Pack window fit ---------------------------------------------------------


def test_pack_window_rejects_unit_when_approach_travel_no_longer_fits() -> None:
   walk_graph = load_walk_graph()
   window_start_seconds = _seconds( '9:00 AM' )
   # 5 minutes fits dwell-only (300s) but not entrance approach (360s) + dwell.
   window_end_seconds = _seconds( '9:05 AM' )
   indo_unit = _prepared_loop_unit(
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      duration_seconds=300 )

   packed_units = LoopWindowPacker.pack(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds ),
      prepared_units=[ indo_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=str( walk_graph[ 'entrance_node_id' ] ) )

   assert packed_units == []


def test_pack_window_accepts_unit_when_window_covers_approach_and_dwell() -> None:
   walk_graph = load_walk_graph()
   window_start_seconds = _seconds( '9:00 AM' )
   window_end_seconds = _seconds( '9:11 AM' )
   indo_unit = _prepared_loop_unit(
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      duration_seconds=300 )

   packed_units = LoopWindowPacker.pack(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds ),
      prepared_units=[ indo_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=str( walk_graph[ 'entrance_node_id' ] ) )

   assert [ unit.unit.loop_id for unit in packed_units ] == [ 'indo_malaya' ]


def test_pack_window_from_entry_node_keeps_dwell_only_fit() -> None:
   walk_graph = load_walk_graph()
   window_start_seconds = _seconds( '9:00 AM' )
   window_end_seconds = _seconds( '9:05 AM' )
   indo_unit = _prepared_loop_unit(
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      duration_seconds=300 )
   entry_node_id = indo_unit.unit.entry_walk_node_id
   assert entry_node_id is not None

   packed_units = LoopWindowPacker.pack(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds ),
      prepared_units=[ indo_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=entry_node_id )

   assert [ unit.unit.loop_id for unit in packed_units ] == [ 'indo_malaya' ]


# --- Single-item scheduling --------------------------------------------------


def test_auto_schedule_delays_first_animal_by_entrance_travel(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='10:00',
      animals=[ GRIZZLY_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=GRIZZLY_KEY )

   walk_graph = load_walk_graph()
   expected_travel_seconds = WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      GRIZZLY_WALK_NODE_ID )

   assert result.success
   assert result.itinerary.arrival_time == '10:00 AM'
   assert result.itinerary.animals[ 0 ].start_time == schedule_time_after_seconds(
      '10:00 AM',
      expected_travel_seconds )
   assert expected_travel_seconds >= 30 * 60


def test_explicit_start_at_arrival_rejected_when_entrance_travel_required(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   rejected = schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='09:30' )

   assert not rejected.success
   assert rejected.status == ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE


def test_explicit_start_accepted_after_entrance_travel(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   expected_start = schedule_time_after_seconds( '9:30 AM', LION_TRAVEL_SECONDS )
   result = schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time=expected_start )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == expected_start


def test_explicit_start_flush_against_previous_animal_rejected(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   lion_start = schedule_time_after_seconds( '9:30 AM', LION_TRAVEL_SECONDS )
   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time=lion_start,
   ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   lion = next(
      animal for animal in itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.end_time is not None

   rejected = schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY,
      start_time=lion.end_time )

   assert not rejected.success
   assert rejected.status == ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE


def test_auto_schedule_second_animal_starts_after_previous_end_plus_travel(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY )

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   penguin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin' )
   travel_seconds = _travel_seconds_between_animals(
      from_species='African Lion',
      from_exhibit='Africa Savanna',
      to_species='African Penguin',
      to_exhibit='Africa Savanna',
      to_enclosure_name='Outdoor' )

   assert result.success
   assert travel_seconds > 0
   assert penguin.start_time == schedule_time_after_seconds(
      lion.end_time,
      travel_seconds )
   assert _seconds( penguin.start_time ) > _seconds( lion.end_time )


def test_auto_schedule_attraction_after_animal_includes_travel(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
   ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL )

   lion = result.itinerary.animals[ 0 ]
   carousel = next(
      attraction for attraction in result.itinerary.attractions
      if attraction.name == CAROUSEL )
   walk_graph = load_walk_graph()
   lion_node_id = walk_node_id_for_viewing_spot(
      'African Lion',
      'Africa Savanna',
      None )
   carousel_node = walk_node_for_map_location(
      MapLocationKind.ATTRACTION,
      CAROUSEL )
   assert lion_node_id is not None
   assert carousel_node is not None
   travel_seconds = WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      lion_node_id,
      carousel_node.walk_node_id )

   assert result.success
   assert travel_seconds > 0
   assert carousel.start_time == schedule_time_after_seconds(
      lion.end_time,
      travel_seconds )


def test_auto_schedule_animal_after_zoomobile_transportation_includes_travel(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name=ZOOMOBILE,
            added_as_attraction=True ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert schedule_itinerary_item(
      item_type='attractions',
      key=ZOOMOBILE,
      start_time='10:00 AM',
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
   )

   lion = result.itinerary.animals[ 0 ]
   zoomobile = result.itinerary.transportations[ 0 ]
   walk_graph = load_walk_graph()
   zoomobile_node_id = TransportationWalkNodeResolver.resolve(
      ZOOMOBILE,
      legs=zoomobile.legs )
   lion_node_id = walk_node_id_for_viewing_spot(
      'African Lion',
      'Africa Savanna',
      None )
   assert zoomobile_node_id is not None
   assert lion_node_id is not None
   travel_seconds = WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      zoomobile_node_id,
      lion_node_id )

   assert result.success
   assert travel_seconds > 0
   assert lion.start_time == schedule_time_after_seconds(
      zoomobile.end_time,
      travel_seconds )


def test_bulk_schedule_animal_then_zoomobile_includes_travel(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name=ZOOMOBILE,
            added_as_attraction=True ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()
   lion = result.itinerary.animals[ 0 ]
   zoomobile = result.itinerary.transportations[ 0 ]
   walk_graph = load_walk_graph()
   lion_node_id = walk_node_id_for_viewing_spot(
      'African Lion',
      'Africa Savanna',
      None )
   zoomobile_node_id = TransportationWalkNodeResolver.resolve( ZOOMOBILE )

   assert result.success
   assert lion.start_time is not None
   assert lion.end_time is not None
   assert zoomobile.start_time is not None
   assert zoomobile.end_time is not None
   assert lion_node_id is not None
   assert zoomobile_node_id is not None

   if _seconds( lion.start_time ) < _seconds( zoomobile.start_time ):
      from_node_id = lion_node_id
      to_node_id = zoomobile_node_id
      earlier_end = lion.end_time
      later_start = zoomobile.start_time
   else:
      from_node_id = zoomobile_node_id
      to_node_id = lion_node_id
      earlier_end = zoomobile.end_time
      later_start = lion.start_time

   travel_seconds = WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      from_node_id,
      to_node_id )

   assert travel_seconds > 0
   assert later_start == schedule_time_after_seconds(
      earlier_end,
      travel_seconds )


# --- Bulk scheduling ---------------------------------------------------------


def test_bulk_schedule_keeps_arrival_at_gate_while_delaying_first_animal(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()
   expected_start = schedule_time_after_seconds( '9:30 AM', LION_TRAVEL_SECONDS )

   assert result.success
   assert result.itinerary.arrival_time == '9:30 AM'
   assert result.itinerary.animals[ 0 ].start_time == expected_start
   assert _seconds( result.itinerary.animals[ 0 ].start_time ) > _seconds(
      result.itinerary.arrival_time )


def test_bulk_schedule_seeds_unset_arrival_to_zoo_open_not_first_animal(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary.arrival_time == '9:30 AM'
   assert result.itinerary.animals[ 0 ].start_time == schedule_time_after_seconds(
      '9:30 AM',
      LION_TRAVEL_SECONDS )


def test_bulk_schedule_places_second_animal_after_inter_stop_travel(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()
   cheetah = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Cheetah' )
   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )

   # Closer Indo-Malaya Cheetah packs first from the entrance.
   assert cheetah.start_time == schedule_time_after_seconds(
      '9:30 AM',
      CHEETAH_INDO_TRAVEL_SECONDS )
   travel_seconds = _travel_seconds_between_animals(
      from_species='Cheetah',
      from_exhibit='Indo-Malaya Outdoor',
      to_species='African Lion',
      to_exhibit='Africa Savanna' )
   assert lion.start_time == schedule_time_after_seconds(
      cheetah.end_time,
      travel_seconds )
   assert _seconds( lion.start_time ) - _seconds( cheetah.end_time ) == travel_seconds


def test_bulk_schedule_persists_floored_travel_minutes_on_walk_legs(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='10:00',
      animals=[ GRIZZLY_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()
   walk_graph = load_walk_graph()
   path = shortest_path(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      GRIZZLY_WALK_NODE_ID )
   assert path is not None
   expected_minutes = WalkTravelTimeCalculator.minutes_from_length_px( path.length_px )

   assert result.success
   persisted = ItineraryWalkRouteProvider.fetch_itinerary_walk_route( db.conn )
   assert persisted.legs
   first_leg = persisted.legs[ 0 ]
   assert first_leg.from_item_key == ENTRANCE_ITEM_KEY
   assert first_leg.to_item_key == GRIZZLY_KEY
   assert first_leg.travel_time_minutes == expected_minutes
   assert 30 <= expected_minutes <= 32


def test_bulk_schedule_does_not_pull_arrival_before_zoo_open(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary.arrival_time == '9:30 AM'
   assert _seconds( result.itinerary.arrival_time ) >= _seconds( '9:30 AM' )


def test_bulk_and_single_schedule_agree_on_first_animal_start(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   expected_start = schedule_time_after_seconds( '9:30 AM', LION_TRAVEL_SECONDS )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   single = schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY )
   assert single.success
   assert single.itinerary.animals[ 0 ].start_time == expected_start

   assert unschedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
   ).success
   assert ItineraryCoordinator.get_itinerary().animals[ 0 ].start_time is None

   bulk = ItineraryCoordinator.bulk_schedule_itinerary()
   assert bulk.success
   assert bulk.itinerary.animals[ 0 ].start_time == expected_start
   assert bulk.itinerary.animals[ 0 ].start_time == single.itinerary.animals[ 0 ].start_time


def test_penguin_entrance_travel_differs_from_lion(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   assert LION_TRAVEL_SECONDS != PENGUIN_TRAVEL_SECONDS
   assert PENGUIN_TRAVEL_SECONDS > 0

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ PENGUIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == schedule_time_after_seconds(
      '9:30 AM',
      PENGUIN_TRAVEL_SECONDS )


def test_explicit_start_one_minute_before_travel_ready_is_rejected(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   ready_start = schedule_time_after_seconds( '9:30 AM', LION_TRAVEL_SECONDS )
   too_early = schedule_time_after_seconds( ready_start, -60 )
   rejected = schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time=too_early )

   assert not rejected.success
   assert rejected.status == ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE


def test_early_admission_bulk_delays_from_nine_am_anchor(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   assert ItineraryCoordinator.suppress_itinerary_warning(
      ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP.value ).success

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary.arrival_time == '9:00 AM'
   assert result.itinerary.animals[ 0 ].start_time == schedule_time_after_seconds(
      '9:00 AM',
      LION_TRAVEL_SECONDS )


def test_prepare_loop_schedule_units_adds_inter_stop_travel_to_duration(
      db: DbControllers ) -> None:
   walk_graph = load_walk_graph()
   units = LoopScheduleUnitBuilder.build(
      [
         [
            _animal_record( species='African Lion', exhibit='Africa Savanna' ),
            _animal_record(
               species='African Penguin',
               exhibit='Africa Savanna',
               enclosure_name='Outdoor' ),
         ],
      ] )
   prepared = LoopWindowPacker.prepare_units(
      db.conn,
      units,
      walk_graph=walk_graph )
   assert prepared is not None
   assert len( prepared ) == 1

   viewing_only = prepared[ 0 ].occupied_seconds - LoopUnitTravelTimeCalculator.total_inter_stop_seconds(
      walk_graph,
      units[ 0 ].stops )
   travel = LoopUnitTravelTimeCalculator.total_inter_stop_seconds( walk_graph, units[ 0 ].stops )

   assert travel > 0
   assert prepared[ 0 ].occupied_seconds == viewing_only + travel
   assert prepared[ 0 ].occupied_seconds > viewing_only


def test_bulk_schedule_three_animals_keeps_travel_gaps_along_chain(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()
   scheduled = sorted(
      [
         animal
         for animal in result.itinerary.animals
         if animal.start_time is not None and animal.end_time is not None
      ],
      key=lambda animal: _seconds( animal.start_time ) )

   assert result.success
   assert len( scheduled ) == 3
   assert result.itinerary.arrival_time == '9:30 AM'
   assert _seconds( scheduled[ 0 ].start_time ) > _seconds( '9:30 AM' )

   for earlier, later in zip( scheduled, scheduled[ 1: ] ):
      gap_seconds = _seconds( later.start_time ) - _seconds( earlier.end_time )
      expected_travel = _travel_seconds_between_animals(
         from_species=earlier.species,
         from_exhibit=earlier.exhibit,
         from_enclosure_name=earlier.enclosure_name,
         to_species=later.species,
         to_exhibit=later.exhibit,
         to_enclosure_name=later.enclosure_name )
      assert gap_seconds == expected_travel
      assert gap_seconds >= 0
