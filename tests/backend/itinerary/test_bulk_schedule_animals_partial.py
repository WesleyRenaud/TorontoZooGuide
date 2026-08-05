from __future__ import annotations

from collections.abc import Callable
from datetime import date
from pathlib import Path
from unittest.mock import patch

from itinerary.support import CHEETAH_INDO_MALAYA_ITINERARY_ENTRY, expected_departure_time_for_itinerary, LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY

from api.connection import close_connection
from api.connection import open_connection
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord
from conftest import DbControllers

FIVE_MINUTE_ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-20',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='09:41',
   close_time='09:41',
)


def _bulk_schedule_with_five_minute_zoo_hours() -> ItinerarySaveResult:
   with patch(
         'api.itinerary.scheduling.items.schedule_itinerary_helpers.fetch_zoo_hours_record',
         return_value=FIVE_MINUTE_ZOO_HOURS ):
      return ItineraryCoordinator.bulk_schedule_animals()


def test_bulk_schedule_animals_returns_issue_when_day_runs_out(
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
   ).success

   result = _bulk_schedule_with_five_minute_zoo_hours()

   assert result.success
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [
      'African Penguin',
      'African Lion',
   ]
   assert [ item.location for item in result.reasons[ 0 ].items ] == [
      'Africa Savanna',
      'Africa Savanna',
   ]
   assert result.reasons[ 0 ].items[ 0 ].item_type == ItinerarySaveIssueItemType.ANIMAL

   scheduled_species = {
      animal.species
      for animal in result.itinerary.animals
      if animal.start_time is not None and animal.end_time is not None
   }
   assert scheduled_species == { 'Cheetah' }

   saved = fetch_saved_itinerary( db.conn )
   lion_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' )
   assert lion_row.start_time is None
   assert lion_row.end_time is None


def test_bulk_schedule_animals_does_not_set_departure_when_not_enough_time(
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
   ).success

   assert ItineraryCoordinator.get_itinerary().departure_time is None

   result = _bulk_schedule_with_five_minute_zoo_hours()

   assert result.success
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME )
   assert result.itinerary.departure_time is None


def test_bulk_schedule_animals_does_not_set_arrival_when_not_enough_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """Incomplete bulk must not seed arrival to zoo open / first packed item."""
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryCoordinator.get_itinerary().arrival_time is None
   assert ItineraryCoordinator.get_itinerary().departure_time is None

   result = _bulk_schedule_with_five_minute_zoo_hours()

   assert result.success
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME )
   assert any(
      animal.start_time is not None
      for animal in result.itinerary.animals )
   assert result.itinerary.arrival_time is None
   assert result.itinerary.departure_time is None


def test_bulk_schedule_animals_persists_partial_schedule_after_connection_close(
      db: DbControllers,
      db_path: Path,
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
   ).success

   result = _bulk_schedule_with_five_minute_zoo_hours()

   assert result.success
   assert len( result.reasons ) == 1

   assert db.conn is not None
   close_connection( db.conn )

   reopened = open_connection( db_path=str( db_path ) )
   saved = fetch_saved_itinerary( reopened )
   scheduled_species = {
      row.species
      for row in saved.animal_rows
      if has_itinerary_schedule_times( row.start_time, row.end_time )
   }
   lion_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' )

   close_connection( reopened )

   assert scheduled_species == { 'Cheetah' }
   assert lion_row.start_time is None
   assert lion_row.end_time is None


def test_bulk_schedule_animals_packs_through_zoo_close_despite_early_departure(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='12:20',
      departure_time='15:00',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.reasons == []
   assert all(
      animal.start_time is not None and animal.end_time is not None
      for animal in result.itinerary.animals
   )
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )
