from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CAROUSEL, CHEETAH_INDO_MALAYA_ITINERARY_ENTRY, entrance_travel_seconds_to_animal, LION_ITINERARY_ENTRY, LION_KEY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, schedule_itinerary_item, schedule_time_after_seconds, unschedule_itinerary_item

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.transportation_walk_node_resolver import TransportationWalkNodeResolver
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_schedule_unit_builder import LoopScheduleUnitBuilder
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.map_location_walk_node_lookup import MapLocationWalkNodeLookup
from api.walk_graph.shortest_path_calculator import ShortestPathCalculator
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver
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
   walk_graph = WalkGraphProvider.fetch()
   from_node_id = ViewingSpotWalkNodeIdResolver.resolve(
      from_species,
      from_exhibit,
      from_enclosure_name )
   to_node_id = ViewingSpotWalkNodeIdResolver.resolve(
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

   walk_graph = WalkGraphProvider.fetch()
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
   walk_graph = WalkGraphProvider.fetch()
   lion_node_id = ViewingSpotWalkNodeIdResolver.resolve(
      'African Lion',
      'Africa Savanna',
      None )
   carousel_node = MapLocationWalkNodeLookup.for_map_location(
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
   walk_graph = WalkGraphProvider.fetch()
   zoomobile_node_id = TransportationWalkNodeResolver.resolve(
      ZOOMOBILE,
      legs=zoomobile.legs )
   lion_node_id = ViewingSpotWalkNodeIdResolver.resolve(
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
   walk_graph = WalkGraphProvider.fetch()
   lion_node_id = ViewingSpotWalkNodeIdResolver.resolve(
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
   walk_graph = WalkGraphProvider.fetch()
   path = ShortestPathCalculator.find(
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
