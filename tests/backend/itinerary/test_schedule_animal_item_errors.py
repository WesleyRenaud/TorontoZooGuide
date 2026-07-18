from __future__ import annotations

from collections.abc import Callable
from datetime import date
from unittest.mock import patch

from itinerary.support import ANIMAL_KEY, LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, saved_animal_row, schedule_itinerary_item

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord
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

   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
   ).success

   rejected = schedule_itinerary_item(
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

   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='12:00 PM',
   ).success

   result = schedule_itinerary_item(
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

   result = schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='' )

   assert result.success
   assert len( result.itinerary.events ) == 1
   assert result.itinerary.events[ 0 ].event_type == ItineraryEventType.LUNCH
   assert result.itinerary.events[ 0 ].start_time == '9:30 AM'
   assert result.itinerary.events[ 0 ].end_time == '10:10 AM'


def test_schedule_itinerary_item_extends_arrival_from_late_short_visit_window(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='4:00 PM',
      departure_time='4:05 PM',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_short_visit=True,
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert result.itinerary.animals[ 0 ].end_time == '4:00 PM'
   assert DateValues.time_value_is_before(
      result.itinerary.arrival_time,
      '4:00 PM' )
   assert not DateValues.time_value_is_after(
      result.itinerary.arrival_time,
      result.itinerary.animals[ 0 ].start_time )


def test_schedule_itinerary_item_extends_departure_when_visit_window_is_too_short(
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

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time is not None
   assert result.itinerary.animals[ 0 ].end_time is not None
   assert DateValues.time_value_is_at_or_after(
      result.itinerary.departure_time,
      result.itinerary.animals[ 0 ].end_time )


def test_schedule_itinerary_item_returns_no_available_slot_when_zoo_hours_are_full(
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

   five_minute_zoo_hours = ZooHoursRecord(
      operating_date='2026-06-15',
      early_admission_time=None,
      open_time='09:30',
      last_admission_time='09:35',
      close_time='09:35',
   )

   with patch(
         'api.itinerary.scheduling.items.schedule_itinerary_helpers.fetch_zoo_hours_record',
         return_value=five_minute_zoo_hours ):
      result = schedule_itinerary_item(
         item_type='animals',
         key=ANIMAL_KEY )

   assert not result.success
   assert result.status == ItineraryErrorType.NO_AVAILABLE_SLOT


def test_schedule_itinerary_item_requested_start_after_departure_extends_departure(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='12:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='1:00 PM',
   )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '1:00 PM'
   assert DateValues.time_value_is_at_or_after(
      result.itinerary.departure_time,
      result.itinerary.animals[ 0 ].end_time )


def test_schedule_itinerary_item_packs_after_full_visit_window_and_extends_departure(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='09:38',
      animals=[ LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_short_visit=True,
   ).success

   lion_result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
   )
   assert lion_result.success
   lion = next(
      animal for animal in lion_result.itinerary.animals
      if animal.species == 'African Lion'
   )

   result = schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY,
   )

   assert result.success
   penguin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin'
   )
   assert penguin.start_time is not None
   assert penguin.end_time is not None
   assert penguin.start_time == lion.end_time
   assert DateValues.time_value_is_at_or_after(
      result.itinerary.departure_time,
      penguin.end_time )


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

   result = schedule_itinerary_item(
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

   result = schedule_itinerary_item(
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
   assert saved_row.is_added is False


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

   result = schedule_itinerary_item(
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
   assert saved_row.is_added is False


def test_schedule_itinerary_item_honors_duration_without_time(
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
      duration_minutes=20 )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '9:30 AM'
   assert result.itinerary.animals[ 0 ].end_time == '9:50 AM'


def test_schedule_itinerary_item_requires_visit_date(
      db: DbControllers ) -> None:
   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert not result.success
   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def test_schedule_already_scheduled_animal_returns_item_already_scheduled(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   first = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   )

   assert first.success
   lion_before = first.itinerary.animals[ 0 ]
   assert lion_before.start_time == '10:00 AM'

   second = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
   )

   assert not second.success
   assert second.status == ItineraryErrorType.ITEM_ALREADY_SCHEDULED
   lion_after = second.itinerary.animals[ 0 ]
   assert lion_after.start_time == lion_before.start_time
   assert lion_after.end_time == lion_before.end_time


def test_schedule_already_scheduled_lunch_returns_item_already_scheduled(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   first = schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='',
      start_time='12:00',
   )

   assert first.success
   lunch_before = first.itinerary.events[ 0 ]
   assert lunch_before.start_time is not None

   second = schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='',
   )

   assert not second.success
   assert second.status == ItineraryErrorType.ITEM_ALREADY_SCHEDULED
   lunch_after = second.itinerary.events[ 0 ]
   assert lunch_after.start_time == lunch_before.start_time
   assert lunch_after.end_time == lunch_before.end_time
