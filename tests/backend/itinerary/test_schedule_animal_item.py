from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import ANIMAL_KEY, expected_departure_time_for_itinerary, LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, schedule_itinerary_item
from itinerary.support import entrance_travel_seconds_to_animal
from itinerary.support import schedule_time_after_seconds
from itinerary.support import schedule_time_before_seconds

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver
from conftest import DbControllers

LION_TRAVEL_SECONDS = entrance_travel_seconds_to_animal(
   species='African Lion',
   exhibit='Africa Savanna' )


def _lion_start_after( anchor_time: str ) -> str:
   return schedule_time_after_seconds( anchor_time, LION_TRAVEL_SECONDS )


def _lion_end_after( anchor_time: str, *, duration_seconds: int = 8 * 60 ) -> str:
   return schedule_time_after_seconds(
      _lion_start_after( anchor_time ),
      duration_seconds )


def _travel_seconds_between_animals(
      *,
      from_species: str,
      from_exhibit: str,
      from_enclosure_name: str | None,
      to_species: str,
      to_exhibit: str,
      to_enclosure_name: str | None ) -> int:
   walk_graph = load_walk_graph()
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
   expected_start = _lion_start_after( '9:30 AM' )
   expected_end = _lion_end_after( '9:30 AM' )
   assert result.itinerary.animals[ 0 ].start_time == expected_start
   assert result.itinerary.animals[ 0 ].end_time == expected_end
   assert result.itinerary.arrival_time == schedule_time_before_seconds(
      expected_start,
      LION_TRAVEL_SECONDS )
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


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
   expected_start = _lion_start_after( '9:30 AM' )
   expected_end = _lion_end_after( '9:30 AM' )
   assert animal.start_time == expected_start
   assert animal.end_time == expected_end
   assert result.itinerary.arrival_time == schedule_time_before_seconds(
      expected_start,
      LION_TRAVEL_SECONDS )
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


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
   assert result.itinerary.animals[ 0 ].start_time == _lion_start_after( '9:00 AM' )
   assert result.itinerary.animals[ 0 ].end_time == _lion_end_after( '9:00 AM' )


def test_set_itinerary_keeps_early_admission_seeded_departure_when_adding_exhibit_animals(
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
   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY ).success

   scheduled = ItineraryCoordinator.get_itinerary()

   assert scheduled.arrival_time == '9:00 AM'
   assert scheduled.departure_time == expected_departure_time_for_itinerary( scheduled )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time=scheduled.arrival_time,
      departure_time=scheduled.departure_time,
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
      confirming_short_visit=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert {
      animal.species
      for animal in result.itinerary.animals
   } == { 'African Lion', 'African Penguin' }


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

   start_time = _lion_start_after( '9:00 AM' )
   result = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time=start_time )

   assert result.success
   assert result.itinerary.animals[ 0 ].start_time == start_time
   assert result.itinerary.animals[ 0 ].end_time == _lion_end_after( '9:00 AM' )


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
   assert result.itinerary.arrival_time == '9:00 AM'
   assert result.itinerary.animals[ 0 ].start_time == _lion_start_after( '9:00 AM' )
   assert result.itinerary.animals[ 0 ].end_time == _lion_end_after( '9:00 AM' )


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
   assert scheduled.itinerary.animals[ 0 ].start_time == _lion_start_after( '9:00 AM' )

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
   animal_start_seconds = DateValues.time_value_in_seconds(
      result.itinerary.animals[ 0 ].start_time )
   open_seconds = DateValues.time_value_in_seconds( '9:30 AM' )
   assert animal_start_seconds is not None
   assert open_seconds is not None
   assert animal_start_seconds >= open_seconds
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
      departure_time='18:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_short_visit=True,
   )

   assert result.success
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )
   assert result.itinerary.animals[ 0 ].start_time == _lion_start_after( '9:30 AM' )
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
   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion'
   )
   scheduled = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin'
   )
   travel_seconds = _travel_seconds_between_animals(
      from_species='African Lion',
      from_exhibit='Africa Savanna',
      from_enclosure_name=None,
      to_species='African Penguin',
      to_exhibit='Africa Savanna',
      to_enclosure_name='Outdoor' )
   assert scheduled.start_time == schedule_time_after_seconds(
      lion.end_time,
      travel_seconds )


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
   expected_start = _lion_start_after( '9:30 AM' )
   expected_end = schedule_time_after_seconds( expected_start, 30 )
   assert result.itinerary.animals[ 0 ].start_time == expected_start
   assert result.itinerary.animals[ 0 ].end_time == expected_end

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

   assert refreshed_itinerary.animals[ 0 ].start_time == expected_start
   assert refreshed_itinerary.animals[ 0 ].end_time == expected_end


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
