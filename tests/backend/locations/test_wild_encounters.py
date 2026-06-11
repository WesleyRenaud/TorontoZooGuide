from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

def test_wild_encounter_schedule_and_cancellation(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='14:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )
   assert encounter.is_available is True
   assert encounter.maximum_duration == 45
   assert encounter.end_time == '14:45'

   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name='African Rainforest',
      date='2026-06-15',
      time='14:00'
   )
   encounters_after_cancel = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   cancelled = next( item for item in encounters_after_cancel if item.name == 'African Rainforest' and item.start_time == '14:00' )
   assert cancelled.is_available is False

   weekday_unavailable = next(
      item for item in WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=16, year=2026 )
      if item.name == 'African Rainforest' and item.start_time == '14:00'
   )
   out_of_range = next(
      item for item in WildEncounterCoordinator.get_wild_encounter_schedule( month='July', day=1, year=2026 )
      if item.name == 'African Rainforest' and item.start_time == '14:00'
   )
   assert weekday_unavailable.unavailable_message == 'African Rainforest is not offered on this day of the week.'
   assert out_of_range.unavailable_message == 'African Rainforest is not scheduled on July 1.'


def test_wild_encounter_search_only_returns_available_schedule_days(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Mischevious Meerkats',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='14:00',
      monday=True,
      tuesday=False,
      wednesday=True,
      thursday=True,
      friday=False,
      saturday=True,
      sunday=False,
      message=None
   )

   monday_results = WildEncounterCoordinator.get_wild_encounters_matching_query(
      query='Mischevious Meerkats',
      month='June',
      day=15,
      year=2026 )
   sunday_results = WildEncounterCoordinator.get_wild_encounters_matching_query(
      query='Mischevious Meerkats',
      month='June',
      day=21,
      year=2026 )
   sunday_available = WildEncounterCoordinator.get_available_wild_encounters(
      month='June',
      day=21,
      year=2026 )

   assert [ item.name for item in monday_results ] == [ 'Mischevious Meerkats' ]
   assert sunday_results == []
   assert all( item.name != 'Mischevious Meerkats' for item in sunday_available )


def test_wild_encounter_occurrences_cover_all_weekdays_and_cancellations(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-15',
      end_date='2026-06-21',
      encounter_time='14:00',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      message=None
   )
   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name='African Rainforest',
      date='2026-06-18',
      time='14:00'
   )

   occurrences = WildEncounterCoordinator.get_wild_encounter_occurrences(
      wild_encounter_name='African Rainforest',
      days_ahead=6
   )

   assert { occurrence.date for occurrence in occurrences } == {
      '2026-06-15',
      '2026-06-16',
      '2026-06-17',
      '2026-06-19',
      '2026-06-20',
      '2026-06-21'
   }
   assert WildEncounterCoordinator.get_wild_encounter_occurrences( wild_encounter_name='' ) == []
   assert WildEncounterCoordinator.get_wild_encounter_occurrences( wild_encounter_name='Bad Encounter' ) == []


