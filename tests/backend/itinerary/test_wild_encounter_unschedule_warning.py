from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import schedule_itinerary_item, wild_encounter_key, wild_encounter_wire
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.data_access.itinerary_walk_route_matcher import ItineraryWalkRouteMatcher
from api.itinerary.data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from api.itinerary.routing.build_itinerary_walk_route import build_itinerary_walk_route
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

ANIMAL_KEY = 'African Lion||Africa Savanna'
WILD_ENCOUNTER = 'African Rainforest'
LION_ITINERARY_ENTRY = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}


def _set_wild_encounter_schedule(
      *,
      encounter_time: str = '14:00' ) -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( encounter_time ),
      message=None,
   )


def _set_itinerary_with_scheduled_animal(
      db: DbControllers,
      *,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='14:00',
   ).success


def test_set_itinerary_returns_warning_when_wild_encounter_would_unschedule_items(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_wild_encounter_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER ) ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ WILD_ENCOUNTER ]

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time == '2:00 PM'
   assert animal.end_time == '2:08 PM'
   assert saved.wild_encounter_names() == []


def test_set_itinerary_unschedules_overlapping_items_when_wild_encounter_confirmed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_wild_encounter_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER ) ],
      confirming_wild_encounter_unschedule=True,
   )

   assert result.success
   assert len( result.itinerary.wild_encounters ) == 1
   assert result.itinerary.wild_encounters[ 0 ].start_time == '2:00 PM'
   assert result.itinerary.wild_encounters[ 0 ].end_time == '2:45 PM'

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.start_time is not None
   assert lion.end_time is not None
   assert DateValues.time_value_in_seconds( lion.end_time ) <= DateValues.time_value_in_seconds( '2:00 PM' )


def test_schedule_wild_encounter_returns_warning_when_it_would_unschedule_items(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_wild_encounter_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = schedule_itinerary_item(
      item_type='wild_encounters',
      key=wild_encounter_wire( WILD_ENCOUNTER ),
   )

   assert not result.success
   assert result.status == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ WILD_ENCOUNTER ]

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time == '2:00 PM'
   assert saved.wild_encounter_names() == []


def test_schedule_wild_encounter_unschedules_overlapping_items_when_confirmed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_wild_encounter_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = schedule_itinerary_item(
      item_type='wild_encounters',
      key=wild_encounter_wire( WILD_ENCOUNTER ),
      confirming_wild_encounter_unschedule=True,
   )

   assert result.success

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.start_time is not None
   assert lion.end_time is not None
   assert DateValues.time_value_in_seconds( lion.end_time ) <= DateValues.time_value_in_seconds( '2:00 PM' )

   encounter = next(
      saved_encounter for saved_encounter in result.itinerary.wild_encounters
      if saved_encounter.name == WILD_ENCOUNTER )
   assert encounter.start_time == '2:00 PM'
   assert encounter.end_time == '2:45 PM'


def test_confirmed_wild_encounter_reschedule_persists_walk_route(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_wild_encounter_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = schedule_itinerary_item(
      item_type='wild_encounters',
      key=wild_encounter_wire( WILD_ENCOUNTER ),
      confirming_wild_encounter_unschedule=True,
   )

   assert result.success

   expected_route = build_itinerary_walk_route( result.itinerary )
   persisted_route = ItineraryWalkRouteProvider.fetch_itinerary_walk_route( db.conn )

   assert ItineraryWalkRouteMatcher.matches( expected_route, persisted_route )
   assert any(
      stop.item_key == WILD_ENCOUNTER
      for stop in persisted_route.stops )


def test_wild_encounter_unschedule_warning_cannot_be_suppressed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_wild_encounter_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   ItineraryStatusProvider.suppress_itinerary_status(
      db.conn,
      ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER ) ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ WILD_ENCOUNTER ]
