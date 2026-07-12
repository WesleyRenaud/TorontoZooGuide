from __future__ import annotations

from collections.abc import Callable
from datetime import date

from wild_encounter_schedule_support import wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_records_for_talk
from conftest import DbControllers


def _june_schedule(
      *,
      start_date: str = '2026-06-01',
      end_date: str = '2026-06-30',
      message: str = 'June schedule.' ) -> dict:
   return {
      'talk': 'African Lion',
      'location': 'Africa Savanna',
      'start_date': start_date,
      'end_date': end_date,
      'schedule_rows': wire_schedule_rows( '10:00' ),
      'message': message,
   }


def test_guardians_talk_schedule_rejects_overlapping_date_ranges(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert GuardiansCoordinator.set_guardians_talk_schedule( **_june_schedule() )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      **_june_schedule(
         start_date='2026-06-15',
         end_date='2026-07-15',
         message='Overlapping schedule.' )
   ) is False
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      **_june_schedule(
         start_date='2026-07-01',
         end_date='2026-07-31',
         message='July schedule.' )
   )


def test_guardians_talk_schedule_can_replace_overlapping_schedules(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert GuardiansCoordinator.set_guardians_talk_schedule( **_june_schedule() )
   assert GuardiansCoordinator.replace_guardians_talk_schedule_overlaps(
      **_june_schedule(
         start_date='2026-06-15',
         end_date='2026-07-15',
         message='Replacement schedule.' )
   )

   schedule_records = fetch_guardians_talk_schedule_records_for_talk(
      db.conn,
      talk_name='African Lion',
      location='Africa Savanna' )

   assert [
      (
         record.schedule_start_date,
         record.schedule_end_date,
         record.talk_time,
      )
      for record in schedule_records
   ] == [
      (
         '2026-06-15',
         '2026-07-15',
         '10:00 AM',
      )
   ]


def test_guardians_talk_schedule_can_trim_existing_schedule_around_new_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert GuardiansCoordinator.set_guardians_talk_schedule(
      **_june_schedule(
         end_date='2026-07-31',
         message='Summer schedule.' )
   )
   assert GuardiansCoordinator.trim_guardians_talk_schedule_overlaps(
      **_june_schedule(
         start_date='2026-06-15',
         end_date='2026-06-20',
         message='Special schedule.' )
   )

   schedule_records = fetch_guardians_talk_schedule_records_for_talk(
      db.conn,
      talk_name='African Lion',
      location='Africa Savanna' )

   assert [
      (
         record.schedule_start_date,
         record.schedule_end_date,
         record.talk_time,
      )
      for record in schedule_records
   ] == [
      (
         '2026-06-01',
         '2026-06-14',
         '10:00 AM',
      ),
      (
         '2026-06-15',
         '2026-06-20',
         '10:00 AM',
      ),
      (
         '2026-06-21',
         '2026-07-31',
         '10:00 AM',
      ),
   ]


def test_guardians_talk_schedule_allows_overlapping_dates_at_different_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert GuardiansCoordinator.set_guardians_talk_schedule( **_june_schedule() )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      **{
         **_june_schedule( message='Later talk.' ),
         'schedule_rows': wire_schedule_rows( '11:00' ),
      }
   )
