from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import ANIMAL_KEY, LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, saved_animal_row

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from conftest import DbControllers


def test_schedule_itinerary_animal_rejects_unavailable_requested_start_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
   ).success

   rejected = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY,
      start_time='09:30',
   )

   assert not rejected.success
   assert rejected.status == ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE

   penguin = next(
      animal for animal in rejected.itinerary.animals
      if animal.species == 'African Penguin'
   )

   assert penguin.start_time is None


def test_schedule_itinerary_animal_rejects_conflicting_noon_start_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='12:00 PM',
   ).success

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY,
      start_time='12:00 PM',
   )

   assert not result.success
   assert result.status == ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE

   penguin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin'
   )

   assert penguin.start_time is None


def test_schedule_itinerary_event_uses_default_duration(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='' )

   assert result.success
   assert len( result.itinerary.events ) == 1
   assert result.itinerary.events[ 0 ].event_type == ItineraryEventType.LUNCH
   assert result.itinerary.events[ 0 ].start_time == '09:30'
   assert result.itinerary.events[ 0 ].end_time == '10:10'


def test_schedule_itinerary_item_returns_no_available_slot(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='09:35',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_short_visit=True,
   ).success

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert not result.success
   assert result.status == ItineraryErrorType.NO_AVAILABLE_SLOT


def test_schedule_itinerary_animal_requires_existing_itinerary_row(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert not result.success
   assert result.status == ItineraryErrorType.ITEM_NOT_ON_ITINERARY
   assert result.itinerary.animals == []


def test_schedule_itinerary_animal_adds_and_schedules_when_confirmed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      confirming_schedule_item_not_on_itinerary=True )

   assert result.success
   assert len( result.itinerary.animals ) == 1
   assert result.itinerary.animals[ 0 ].start_time is not None
   saved_row = saved_animal_row(
      db,
      species=LION_ITINERARY_ENTRY[ 'species' ],
      exhibit=LION_ITINERARY_ENTRY[ 'exhibit' ] )
   assert saved_row.new_likelihood is None
   assert saved_row.old_likelihood is None
   assert saved_row.is_added is True


def test_schedule_itinerary_animal_adds_and_schedules_when_warning_suppressed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   ItineraryCoordinator.suppress_itinerary_warning(
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY.value )

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert result.suppressed_warnings == (
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
   )
   assert len( result.itinerary.animals ) == 1
   saved_row = saved_animal_row(
      db,
      species=LION_ITINERARY_ENTRY[ 'species' ],
      exhibit=LION_ITINERARY_ENTRY[ 'exhibit' ] )
   assert saved_row.new_likelihood is None
   assert saved_row.is_added is True


def test_schedule_itinerary_item_rejects_duration_without_time(
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

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      duration_minutes=20 )

   assert not result.success
   assert result.status == ItineraryErrorType.SAVE_FAILED


def test_schedule_itinerary_item_requires_visit_date(
      db: DbControllers ) -> None:
   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert not result.success
   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET
