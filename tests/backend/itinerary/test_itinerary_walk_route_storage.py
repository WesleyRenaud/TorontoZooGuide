from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import ANIMAL_KEY, CHEETAH_ITINERARY_ENTRY, schedule_itinerary_item
from itinerary.support import LION_ITINERARY_ENTRY

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.fetch_itinerary_walk_route import fetch_itinerary_walk_route
from api.itinerary.data_access.itinerary_walk_route_helpers import walk_route_matches
from api.itinerary.results.itinerary_result_response import itinerary_result_to_dict
from api.itinerary.routing.build_itinerary_walk_route import build_itinerary_walk_route
from api.itinerary.routing.itinerary_walk_route import empty_itinerary_walk_route
from api.itinerary.routing.persist_itinerary_walk_route import rebuild_and_persist_itinerary_walk_route
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def test_schedule_itinerary_item_persists_walk_route(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   )

   assert result.success

   expected_route = build_itinerary_walk_route( result.itinerary )
   persisted_route = fetch_itinerary_walk_route( db.conn )

   assert walk_route_matches( expected_route, persisted_route )


def test_bulk_schedule_itinerary_persists_walk_route(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   expected_route = build_itinerary_walk_route( result.itinerary )
   persisted_route = fetch_itinerary_walk_route( db.conn )

   assert walk_route_matches( expected_route, persisted_route )


def test_fetch_itinerary_walk_route_returns_empty_when_unpersisted(
      db: DbControllers ) -> None:
   walk_route = fetch_itinerary_walk_route( db.conn )

   assert walk_route == empty_itinerary_walk_route()


def test_rebuild_and_persist_itinerary_walk_route_round_trips_route(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   ).success

   expected_route = build_itinerary_walk_route(
      ItineraryCoordinator.get_itinerary() )

   assert rebuild_and_persist_itinerary_walk_route(
      db.conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
   )
   persisted_route = fetch_itinerary_walk_route( db.conn )

   assert walk_route_matches( expected_route, persisted_route )


def test_clear_itinerary_clears_walk_route(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   ).success

   assert rebuild_and_persist_itinerary_walk_route(
      db.conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
   )
   assert fetch_itinerary_walk_route( db.conn ).legs

   assert ItineraryCoordinator.clear_itinerary()
   assert fetch_itinerary_walk_route( db.conn ) == empty_itinerary_walk_route()


def test_itinerary_result_to_dict_includes_itinerary_path(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   )

   assert result.success

   payload = itinerary_result_to_dict( result, conn=db.conn )

   assert payload[ 'itinerary_path' ] == fetch_itinerary_walk_route( db.conn ).to_dict()
   assert payload[ 'itinerary_path' ][ 'points' ]


def test_set_itinerary_preserves_walk_route_when_adding_unscheduled_item(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   ).success

   assert fetch_itinerary_walk_route( db.conn ).legs

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time
   assert not result.itinerary.animals[ 1 ].start_time

   expected_route = build_itinerary_walk_route( result.itinerary )
   persisted_route = fetch_itinerary_walk_route( db.conn )
   payload = itinerary_result_to_dict( result, conn=db.conn )

   assert expected_route.legs
   assert walk_route_matches( expected_route, persisted_route )
   assert payload[ 'itinerary_path' ][ 'points' ]
   assert walk_route_matches(
      build_itinerary_walk_route( result.itinerary ),
      fetch_itinerary_walk_route( db.conn ) )
