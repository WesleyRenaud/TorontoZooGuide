from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

def test_set_end_and_cancel_guardians_talk_schedule_changes_talk_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='10:00',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=''
   )

   talks = GuardiansCoordinator.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert any( talk.name == 'African Lion' and talk.start_time == '10:00' for talk in talks )

   assert GuardiansCoordinator.end_guardians_talk_schedule( 'African Lion', 'Africa Savanna', '2026-06-14' )

   talks = GuardiansCoordinator.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert all( not ( talk.name == 'African Lion' and talk.start_time == '10:00' ) for talk in talks )

   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='10:00',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=''
   )
   assert GuardiansCoordinator.cancel_guardians_talk_occurrence( 'African Lion', 'Africa Savanna', '2026-06-15', '10:00' )

   talks = GuardiansCoordinator.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert all( not ( talk.name == 'African Lion' and talk.start_time == '10:00' ) for talk in talks )
   assert GuardiansCoordinator.cancel_guardians_talk_occurrence( 'African Lion', 'Africa Savanna', '2026-06-15', '10:00' ) is False

def test_set_end_and_cancel_wild_encounter_schedule_changes_wild_encounter_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      'African Rainforest',
      '2026-06-01',
      '2026-06-30',
      '14:00',
      True,
      False,
      False,
      False,
      False,
      False,
      False,
      ''
   )

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )

   assert encounter.is_available is True
   assert encounter.unavailable_message is None

   assert WildEncounterCoordinator.end_wild_encounter_schedule( 'African Rainforest', '2026-06-14' )

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )

   assert encounter.is_available is False
   assert encounter.unavailable_message == 'African Rainforest is not scheduled on June 15.'

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      'African Rainforest',
      '2026-06-01',
      '2026-06-30',
      '14:00',
      True,
      False,
      False,
      False,
      False,
      False,
      False,
      ''
   )
   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence( 'African Rainforest', '2026-06-15', '14:00' )

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )

   assert encounter.is_available is False
   assert encounter.unavailable_message == 'African Rainforest has been cancelled for this date.'
   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence( 'African Rainforest', '2026-06-15', '14:00' ) is False
