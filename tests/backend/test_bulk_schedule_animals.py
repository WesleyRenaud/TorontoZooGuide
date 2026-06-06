from __future__ import annotations

from collections.abc import Callable
from datetime import date
from pathlib import Path

from api.connection import close_connection
from api.connection import open_connection
from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.logic.bulk_schedule_animals import has_itinerary_schedule_times
from api.itinerary.logic.bulk_schedule_animals import is_itinerary_animal_unscheduled
from api.itinerary.logic.bulk_schedule_animals import sort_animals_for_bulk_schedule
from api.itinerary.logic.bulk_schedule_exhibit_order import bulk_schedule_exhibit_rank
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType
from conftest import DbControllers

LION_ITINERARY_ENTRY = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}
PENGUIN_ITINERARY_ENTRY = {
   'species': 'African Penguin',
   'exhibit': 'Africa Savanna',
}
CHEETAH_INDO_MALAYA_ENTRY = {
   'species': 'Cheetah',
   'exhibit': 'Indo-Malaya Outdoor',
}


def test_sort_animals_for_bulk_schedule_orders_by_exhibit_then_species() -> None:
   animals = sort_animals_for_bulk_schedule( [
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
      ),
      ItineraryAnimalRecord(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         old_likelihood=None,
         new_likelihood=100,
      ),
      ItineraryAnimalRecord(
         species='African Penguin',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
      ),
   ] )

   assert [ ( animal.species, animal.exhibit ) for animal in animals ] == [
      ( 'Cheetah', 'Indo-Malaya Outdoor' ),
      ( 'African Lion', 'Africa Savanna' ),
      ( 'African Penguin', 'Africa Savanna' ),
   ]


def test_bulk_schedule_exhibit_rank_orders_americas_pavilion_before_mayan_temple() -> None:
   assert bulk_schedule_exhibit_rank( 'Americas Pavilion' ) < bulk_schedule_exhibit_rank(
      'Americas Outdoor Mayan Temple Ruins' )


def test_is_itinerary_animal_unscheduled() -> None:
   assert is_itinerary_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
      )
   )
   assert is_itinerary_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
         start_time='',
         end_time='',
      )
   )
   assert not is_itinerary_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
         start_time='09:30',
         end_time='09:38',
      )
   )
   assert not has_itinerary_schedule_times( '09:30', None )
   assert not has_itinerary_schedule_times( None, '09:38' )


def test_bulk_schedule_animals_schedules_in_exhibit_order(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == ()

   cheetah = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Cheetah' )
   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )

   assert cheetah.start_time == '09:30'
   assert lion.start_time == '09:35'
   assert cheetah.end_time is not None
   assert lion.end_time is not None


def test_bulk_schedule_animals_skips_already_scheduled_animals(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key='African Lion||Africa Savanna',
   ).success

   result = ItineraryController.bulk_schedule_animals()

   assert result.success
   assert result.reasons == ()

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   penguin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin' )

   assert lion.start_time == '09:00'
   assert lion.end_time is not None
   assert penguin.start_time == '09:08'
   assert penguin.end_time is not None


def test_bulk_schedule_animals_warns_when_all_animals_are_already_scheduled(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key='African Lion||Africa Savanna',
   ).success
   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key='African Penguin||Africa Savanna',
   ).success

   result = ItineraryController.bulk_schedule_animals()

   assert not result.success
   assert result.status == ItineraryErrorType.BULK_SCHEDULE_ANIMALS_ALREADY_SCHEDULED
   assert result.reasons == ()
   assert {
      animal.species
      for animal in result.itinerary.animals
      if has_itinerary_schedule_times( animal.start_time, animal.end_time )
   } == { 'African Lion', 'African Penguin' }


def test_bulk_schedule_animals_returns_issue_when_day_runs_out(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='09:35',
      confirming_short_visit=True,
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.bulk_schedule_animals()

   assert result.success
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [
      'African Lion',
      'African Penguin',
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
   penguin_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Penguin' )
   assert penguin_row.start_time is None
   assert penguin_row.end_time is None


def test_bulk_schedule_animals_persists_partial_schedule_after_connection_close(
      db: DbControllers,
      db_path: Path,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='09:35',
      confirming_short_visit=True,
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.bulk_schedule_animals()

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
   penguin_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Penguin' )

   close_connection( reopened )

   assert scheduled_species == { 'Cheetah' }
   assert penguin_row.start_time is None
   assert penguin_row.end_time is None


def test_bulk_schedule_animals_requires_visit_date(
      db: DbControllers ) -> None:
   result = ItineraryController.bulk_schedule_animals()

   assert not result.success
   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def test_bulk_schedule_animals_with_no_unscheduled_animals(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.bulk_schedule_animals()

   assert result.success
   assert result.reasons == ()
   assert result.itinerary.animals == []
