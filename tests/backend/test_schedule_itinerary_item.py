from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.logic.parse_schedule_item_request import parse_schedule_item_request
from api.itinerary.scheduling.find_next_available_slot import find_next_available_slot
from api.itinerary.scheduling.scheduling_anchor import scheduling_anchor_minutes
from api.itinerary.scheduling.time_block import time_blocks_overlap
from api.itinerary.scheduling.time_block import TimeBlock
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record
from conftest import DbControllers

ANIMAL_KEY = 'African Lion||Africa Savanna'
PENGUIN_KEY = 'African Penguin||Africa Savanna'
LION_ITINERARY_ENTRY = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}
PENGUIN_ITINERARY_ENTRY = {
   'species': 'African Penguin',
   'exhibit': 'Africa Savanna',
}


def test_parse_schedule_item_request_animal_key() -> None:
   parsed = parse_schedule_item_request( 'animals', ANIMAL_KEY )

   assert parsed is not None
   assert parsed.kind == 'animal'
   assert parsed.species == 'African Lion'
   assert parsed.exhibit == 'Africa Savanna'


def test_parse_schedule_item_request_event_type_as_item_type() -> None:
   parsed = parse_schedule_item_request( 'lunch', '' )

   assert parsed is not None
   assert parsed.kind == 'event'
   assert parsed.event_type == ItineraryEventType.LUNCH


def test_parse_schedule_item_request_attraction_key() -> None:
   parsed = parse_schedule_item_request( 'attractions', 'Conservation Carousel' )

   assert parsed is not None
   assert parsed.kind == 'attraction'
   assert parsed.attraction_name == 'Conservation Carousel'


def test_scheduling_anchor_uses_arrival_when_set( db: DbControllers ) -> None:
   zoo_hours = fetch_zoo_hours_record( db.conn, date( 2026, 6, 20 ) )

   assert scheduling_anchor_minutes( zoo_hours, '09:00' ) == 9 * 60
   assert scheduling_anchor_minutes( zoo_hours, None ) == 9 * 60 + 30


def test_scheduling_anchor_ignores_early_admission_without_arrival(
      db: DbControllers ) -> None:
   zoo_hours = fetch_zoo_hours_record( db.conn, date( 2026, 6, 20 ) )

   assert zoo_hours.early_admission_time == '09:00'
   assert zoo_hours.open_time == '09:30'
   assert scheduling_anchor_minutes( zoo_hours, None ) == 9 * 60 + 30


def test_find_next_available_slot_skips_overlapping_blockers() -> None:
   blockers = [
      TimeBlock( start_minutes=9 * 60 + 30, end_minutes=9 * 60 + 38 ),
   ]

   slot = find_next_available_slot(
      blockers,
      anchor_minutes=9 * 60 + 30,
      duration_minutes=8,
      day_end_minutes=17 * 60 )

   assert slot == ( '09:45', '09:53' )


def test_find_next_available_slot_returns_none_when_window_is_too_short() -> None:
   assert find_next_available_slot(
      [],
      anchor_minutes=9 * 60 + 30,
      duration_minutes=8,
      day_end_minutes=9 * 60 + 35,
   ) is None


def test_schedule_itinerary_animal_uses_open_time_without_arrival(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert len( result.itinerary.animals ) == 1
   assert result.itinerary.animals[ 0 ].start_time == '09:30'
   assert result.itinerary.animals[ 0 ].end_time == '09:38'


def test_schedule_itinerary_animal_uses_arrival_time_when_set(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '09:00'
   assert result.itinerary.animals[ 0 ].end_time == '09:08'


def test_schedule_itinerary_animal_skips_existing_scheduled_slot(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
   ).success

   result = ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY )

   assert result.success
   scheduled = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin'
   )

   assert scheduled.start_time == '09:45'


def test_schedule_itinerary_event_uses_default_duration(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.schedule_itinerary_item(
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

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='09:35',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_short_visit=True,
   ).success

   result = ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert not result.success
   assert result.error_type == ItineraryErrorType.NO_AVAILABLE_SLOT


def test_schedule_itinerary_animal_requires_existing_itinerary_row(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert not result.success
   assert result.error_type == ItineraryErrorType.SAVE_FAILED
   assert result.itinerary.animals == []


def test_schedule_itinerary_item_requires_visit_date(
      db: DbControllers ) -> None:
   result = ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert not result.success
   assert result.error_type == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def test_time_blocks_overlap_allows_adjacent_slots() -> None:
   first = TimeBlock( start_minutes=9 * 60, end_minutes=9 * 60 + 30 )
   second = TimeBlock( start_minutes=9 * 60 + 30, end_minutes=10 * 60 )

   assert not time_blocks_overlap( first, second )
