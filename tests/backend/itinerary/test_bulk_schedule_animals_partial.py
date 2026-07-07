from __future__ import annotations

from collections.abc import Callable
from datetime import date
from pathlib import Path

from itinerary.support import CHEETAH_INDO_MALAYA_ITINERARY_ENTRY, LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY

from api.connection import close_connection
from api.connection import open_connection
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType
from conftest import DbControllers


def test_bulk_schedule_animals_returns_issue_when_day_runs_out(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='09:35',
      confirming_short_visit=True,
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
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [
      'African Lion',
      'Cheetah',
   ]
   assert [ item.location for item in result.reasons[ 0 ].items ] == [
      'Africa Savanna',
      'Indo-Malaya Outdoor',
   ]
   assert result.reasons[ 0 ].items[ 0 ].item_type == ItinerarySaveIssueItemType.ANIMAL

   scheduled_species = {
      animal.species
      for animal in result.itinerary.animals
      if animal.start_time is not None and animal.end_time is not None
   }
   assert scheduled_species == { 'African Penguin' }

   saved = fetch_saved_itinerary( db.conn )
   lion_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' )
   assert lion_row.start_time is None
   assert lion_row.end_time is None


def test_bulk_schedule_animals_persists_partial_schedule_after_connection_close(
      db: DbControllers,
      db_path: Path,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='09:35',
      confirming_short_visit=True,
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

   assert scheduled_species == { 'African Penguin' }
   assert lion_row.start_time is None
   assert lion_row.end_time is None
