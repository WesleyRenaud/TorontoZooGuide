from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import ANIMAL_KEY, LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, schedule_itinerary_item

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_schedule_itinerary_animal_uses_open_time_without_arrival(
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

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert len( result.itinerary.animals ) == 1
   assert result.itinerary.animals[ 0 ].start_time == '9:30 AM'
   assert result.itinerary.animals[ 0 ].end_time == '9:38 AM'
   assert result.itinerary.arrival_time == result.itinerary.animals[ 0 ].start_time
   assert result.itinerary.departure_time == result.itinerary.animals[ 0 ].end_time


def test_schedule_singular_animal_on_date_only_itinerary_seeds_arrival_and_departure(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   before = ItineraryCoordinator.get_itinerary()

   assert before.arrival_time is None
   assert before.departure_time is None

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      confirming_schedule_item_not_on_itinerary=True )

   assert result.success
   assert len( result.itinerary.animals ) == 1
   animal = result.itinerary.animals[ 0 ]
   assert animal.start_time == '9:30 AM'
   assert animal.end_time == '9:38 AM'
   assert result.itinerary.arrival_time == animal.start_time
   assert result.itinerary.departure_time == animal.end_time


def test_schedule_itinerary_animal_uses_early_admission_when_warning_suppressed(
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

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert len( result.itinerary.animals ) == 1
   assert result.itinerary.animals[ 0 ].start_time == '9:00 AM'
   assert result.itinerary.animals[ 0 ].end_time == '9:08 AM'


def test_schedule_itinerary_animal_accepts_explicit_early_admission_start_when_suppressed(
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

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='09:00' )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '9:00 AM'
   assert result.itinerary.animals[ 0 ].end_time == '9:08 AM'


def test_schedule_itinerary_animal_rejects_explicit_early_admission_start_when_not_suppressed(
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

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='09:00' )

   assert not result.success
   assert result.status == ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE


def test_schedule_itinerary_animal_uses_arrival_time_when_set(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '9:00 AM'
   assert result.itinerary.animals[ 0 ].end_time == '9:08 AM'


def test_date_change_reschedules_animal_before_new_admission_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   scheduled = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert scheduled.success
   assert scheduled.itinerary.animals[ 0 ].start_time == '9:00 AM'

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary.arrival_time == '9:30 AM'
   assert result.itinerary.animals[ 0 ].start_time == '9:30 AM'
   assert result.itinerary.animals[ 0 ].end_time is not None


def test_date_change_reschedules_animal_after_new_closing_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='19:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   scheduled = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='18:30' )

   assert scheduled.success
   assert scheduled.itinerary.animals[ 0 ].start_time == '6:30 PM'

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:30',
      departure_time='19:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary.departure_time == '9:38 AM'
   assert result.itinerary.animals[ 0 ].start_time == '9:30 AM'
   assert result.itinerary.animals[ 0 ].end_time is not None


def test_schedule_itinerary_animal_skips_existing_scheduled_slot(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   db.conn.execute(
      """   UPDATE EnclosureViewing
            SET DEFAULT_ITINERARY_DURATION_MINUTES = ?
            WHERE SPECIES = ?
              AND EXHIBIT = ?
              AND NAME = ?;
      """,
      ( 7, 'African Penguin', 'Africa Savanna', 'Outdoor' ) )
   db.conn.commit()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY )

   assert result.success
   scheduled = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin'
   )

   assert scheduled.start_time == '9:38 AM'


def test_schedule_itinerary_animal_preserves_sub_minute_default_duration(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   db.conn.execute(
      """   UPDATE EnclosureViewing
            SET DEFAULT_ITINERARY_DURATION_MINUTES = ?
            WHERE SPECIES = ?
              AND EXHIBIT = ?
              AND NAME IS NULL;
      """,
      ( 0.5, 'African Lion', 'Africa Savanna' ) )
   db.conn.commit()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '9:30 AM'
   assert result.itinerary.animals[ 0 ].end_time == '9:30:30 AM'

   db.conn.execute(
      """   UPDATE EnclosureViewing
            SET DEFAULT_ITINERARY_DURATION_MINUTES = ?
            WHERE SPECIES = ?
              AND EXHIBIT = ?
              AND NAME IS NULL;
      """,
      ( 8, 'African Lion', 'Africa Savanna' ) )
   db.conn.commit()

   refreshed_itinerary = ItineraryCoordinator.get_itinerary()

   assert refreshed_itinerary.animals[ 0 ].start_time == '9:30 AM'
   assert refreshed_itinerary.animals[ 0 ].end_time == '9:30:30 AM'


def test_schedule_itinerary_animal_honors_requested_start_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00' )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '10:00 AM'
   assert result.itinerary.animals[ 0 ].end_time == '10:08 AM'


def test_schedule_itinerary_animal_honors_requested_duration(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
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
      duration_minutes=20 )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '10:00 AM'
   assert result.itinerary.animals[ 0 ].end_time == '10:20 AM'
