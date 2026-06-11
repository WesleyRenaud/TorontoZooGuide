from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.logic.parse_schedule_item_request import parse_schedule_item_request
from api.itinerary.scheduling.find_next_available_slot import find_next_available_slot
from api.itinerary.scheduling.scheduling_anchor import scheduling_anchor_seconds
from api.itinerary.scheduling.time_block import time_blocks_overlap
from api.itinerary.scheduling.time_block import TimeBlock
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.shared.enums import ScheduleItemKind
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


def _saved_animal_row(
      db: DbControllers,
      *,
      species: str,
      exhibit: str ) -> ItineraryAnimalRecord:
   saved_itinerary = fetch_saved_itinerary( db.conn )

   for row in saved_itinerary.animal_rows:
      if row.species == species and row.exhibit == exhibit:
         return row

   raise AssertionError(
      f'Expected saved animal row for { species } / { exhibit }' )


def test_schedule_item_kind_from_item_type_accepts_module_types() -> None:
   assert ScheduleItemKind.from_item_type( 'animals' ) == ScheduleItemKind.ANIMAL
   assert ScheduleItemKind.from_item_type( 'attractions' ) == ScheduleItemKind.ATTRACTION
   assert ScheduleItemKind.ANIMAL.item_type == 'animals'
   assert ScheduleItemKind.ATTRACTION.item_type == 'attractions'


def test_parse_schedule_item_request_animal_key() -> None:
   parsed = parse_schedule_item_request( 'animals', ANIMAL_KEY )

   assert parsed is not None
   assert parsed.kind == ScheduleItemKind.ANIMAL
   assert parsed.species == 'African Lion'
   assert parsed.exhibit == 'Africa Savanna'


def test_parse_schedule_item_request_event_type_as_item_type() -> None:
   parsed = parse_schedule_item_request( 'lunch', '' )

   assert parsed is not None
   assert parsed.kind == ScheduleItemKind.EVENT
   assert parsed.event_type == ItineraryEventType.LUNCH


def test_parse_schedule_item_request_attraction_key() -> None:
   parsed = parse_schedule_item_request( 'attractions', 'Conservation Carousel' )

   assert parsed is not None
   assert parsed.kind == ScheduleItemKind.ATTRACTION
   assert parsed.attraction_name == 'Conservation Carousel'


def test_scheduling_anchor_uses_arrival_when_set( db: DbControllers ) -> None:
   zoo_hours = fetch_zoo_hours_record( db.conn, date( 2026, 6, 20 ) )

   assert scheduling_anchor_seconds( zoo_hours, '09:00' ) == 9 * 3600
   assert scheduling_anchor_seconds( zoo_hours, None ) == 9 * 3600 + 30 * 60


def test_scheduling_anchor_ignores_early_admission_without_arrival(
      db: DbControllers ) -> None:
   zoo_hours = fetch_zoo_hours_record( db.conn, date( 2026, 6, 20 ) )

   assert zoo_hours.early_admission_time == '09:00'
   assert zoo_hours.open_time == '09:30'
   assert scheduling_anchor_seconds( zoo_hours, None ) == 9 * 3600 + 30 * 60


def test_find_next_available_slot_skips_overlapping_blockers() -> None:
   blockers = [
      TimeBlock(
         start_seconds=9 * 3600 + 30 * 60,
         end_seconds=9 * 3600 + 38 * 60 ),
   ]

   slot = find_next_available_slot(
      blockers,
      anchor_seconds=9 * 3600 + 30 * 60,
      duration_seconds=8 * 60,
      day_end_seconds=17 * 3600 )

   assert slot == ( '09:38', '09:46' )


def test_find_next_available_slot_returns_none_when_window_is_too_short() -> None:
   assert find_next_available_slot(
      [],
      anchor_seconds=9 * 3600 + 30 * 60,
      duration_seconds=8 * 60,
      day_end_seconds=9 * 3600 + 35 * 60,
   ) is None


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
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.schedule_itinerary_item(
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

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '09:00'
   assert result.itinerary.animals[ 0 ].end_time == '09:08'


def test_date_change_unschedules_animal_before_new_admission_time(
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

   scheduled = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert scheduled.success
   assert scheduled.itinerary.animals[ 0 ].start_time == '09:00'

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
   assert result.itinerary.arrival_time == '09:30'
   assert result.itinerary.animals[ 0 ].start_time is None
   assert result.itinerary.animals[ 0 ].end_time is None


def test_date_change_unschedules_animal_after_new_closing_time(
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

   scheduled = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='18:30' )

   assert scheduled.success
   assert scheduled.itinerary.animals[ 0 ].start_time == '18:30'

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
   assert result.itinerary.departure_time == '18:00'
   assert result.itinerary.animals[ 0 ].start_time is None
   assert result.itinerary.animals[ 0 ].end_time is None


def test_schedule_itinerary_animal_skips_existing_scheduled_slot(
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

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY )

   assert result.success
   scheduled = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin'
   )

   assert scheduled.start_time == '09:38'


def test_schedule_itinerary_animal_preserves_sub_minute_default_duration(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   db.conn.execute(
      """   UPDATE Enclosure
            SET DEFAULT_ITINERARY_DURATION_MINUTES = ?
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
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

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '09:30'
   assert result.itinerary.animals[ 0 ].end_time == '09:30:30'

   db.conn.execute(
      """   UPDATE Enclosure
            SET DEFAULT_ITINERARY_DURATION_MINUTES = ?
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 8, 'African Lion', 'Africa Savanna' ) )
   db.conn.commit()

   refreshed_itinerary = ItineraryCoordinator.get_itinerary()

   assert refreshed_itinerary.animals[ 0 ].start_time == '09:30'
   assert refreshed_itinerary.animals[ 0 ].end_time == '09:30:30'


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
   saved_row = _saved_animal_row(
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
   saved_row = _saved_animal_row(
      db,
      species=LION_ITINERARY_ENTRY[ 'species' ],
      exhibit=LION_ITINERARY_ENTRY[ 'exhibit' ] )
   assert saved_row.new_likelihood is None
   assert saved_row.is_added is True


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

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00' )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '10:00'
   assert result.itinerary.animals[ 0 ].end_time == '10:08'


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

   result = ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
      duration_minutes=20 )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == '10:00'
   assert result.itinerary.animals[ 0 ].end_time == '10:20'


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


def test_time_blocks_overlap_allows_adjacent_slots() -> None:
   first = TimeBlock( start_seconds=9 * 60 * 60, end_seconds=( 9 * 60 + 30 ) * 60 )
   second = TimeBlock( start_seconds=( 9 * 60 + 30 ) * 60, end_seconds=10 * 60 * 60 )

   assert not time_blocks_overlap( first, second )
