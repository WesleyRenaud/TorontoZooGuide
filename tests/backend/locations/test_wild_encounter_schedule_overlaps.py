from __future__ import annotations

from collections.abc import Callable
from datetime import date

from wild_encounter_schedule_support import wire_schedule_rows

from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.data_access.wild_encounter_schedule import fetch_wild_encounter_schedule_records_for_occurrences
from conftest import DbControllers


def _june_schedule(
      *,
      start_date: str = '2026-06-01',
      end_date: str = '2026-06-30',
      message: str = 'June schedule.' ) -> dict:
   return {
      'wild_encounter_name': 'African Rainforest',
      'start_date': start_date,
      'end_date': end_date,
      'schedule_rows': wire_schedule_rows( '2:00 PM' ),
      'message': message,
   }


def test_wild_encounter_schedule_rejects_overlapping_date_ranges(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule( **_june_schedule() )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      **_june_schedule(
         start_date='2026-06-15',
         end_date='2026-07-15',
         message='Overlapping schedule.' )
   ) is False
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      **_june_schedule(
         start_date='2026-07-01',
         end_date='2026-07-31',
         message='July schedule.' )
   )


def test_wild_encounter_schedule_can_replace_overlapping_schedules(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule( **_june_schedule() )
   assert WildEncounterCoordinator.replace_wild_encounter_schedule_overlaps(
      **_june_schedule(
         start_date='2026-06-15',
         end_date='2026-07-15',
         message='Replacement schedule.' )
   )

   schedule_records = fetch_wild_encounter_schedule_records_for_occurrences(
      db.conn,
      wild_encounter='African Rainforest' )

   assert [
      (
         record.schedule_start_date,
         record.schedule_end_date,
         record.encounter_time,
      )
      for record in schedule_records
   ] == [
      (
         '2026-06-15',
         '2026-07-15',
         '2:00 PM',
      )
   ]


def test_wild_encounter_schedule_can_trim_existing_schedule_around_new_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      **_june_schedule(
         end_date='2026-07-31',
         message='Summer schedule.' )
   )
   assert WildEncounterCoordinator.trim_wild_encounter_schedule_overlaps(
      **_june_schedule(
         start_date='2026-06-15',
         end_date='2026-06-20',
         message='Special schedule.' )
   )

   schedule_records = fetch_wild_encounter_schedule_records_for_occurrences(
      db.conn,
      wild_encounter='African Rainforest' )

   assert [
      (
         record.schedule_start_date,
         record.schedule_end_date,
         record.encounter_time,
      )
      for record in schedule_records
   ] == [
      (
         '2026-06-01',
         '2026-06-14',
         '2:00 PM',
      ),
      (
         '2026-06-15',
         '2026-06-20',
         '2:00 PM',
      ),
      (
         '2026-06-21',
         '2026-07-31',
         '2:00 PM',
      ),
   ]
