from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from conftest import DbControllers

def test_guardians_talk_lookup_queries_return_seed_data( db: DbControllers ) -> None:
   assert GuardiansCoordinator.get_guardians_talk_locations() == [
      'Africa Savanna',
      'African Rainforest Pavilion',
      'Americas Outdoor Mayan Temple Ruins',
      'Americas Pavilion',
      'Australasia Outdoor',
      'Australasia Pavilion',
      'Canadian Domain',
      'Eurasia Wilds',
      'Goat World',
      'Greenhouse',
      'Indo-Malaya Outdoor',
      'Indo-Malaya Pavilion',
      'Tundra Trek',
   ]

   assert 'Komodo Dragon' in GuardiansCoordinator.get_guardians_talk_names()
   assert GuardiansCoordinator.get_guardians_talk_names_at_location(
      'Australasia Pavilion' ) == [ 'Komodo Dragon' ]

   details = GuardiansCoordinator.get_guardians_talk_details()

   assert any( talk.name == 'Komodo Dragon' for talk in details )
   assert any(
      talk.name == 'Komodo Dragon' and talk.location == 'Australasia Pavilion'
      for talk in details )


def test_guardians_talk_schedule_and_cancellation(
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
      message=None
   )

   talks = GuardiansCoordinator.get_guardians_talk_schedule( month='June', day=15, year=2026 )
   assert any( talk.name == 'African Lion' and talk.start_time == '10:00 AM' for talk in talks )
   talk = next(
      talk for talk in talks
      if talk.name == 'African Lion' and talk.start_time == '10:00 AM'
   )
   assert talk.maximum_duration == 30
   assert talk.end_time == '10:30 AM'

   assert GuardiansCoordinator.cancel_guardians_talk_occurrence(
      talk='African Lion',
      location='Africa Savanna',
      date='2026-06-15',
      time='10:00 AM'
   )
   talks_after_cancel = GuardiansCoordinator.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert all( not ( talk.name == 'African Lion' and talk.start_time == '10:00 AM' ) for talk in talks_after_cancel )

   assert GuardiansCoordinator.get_guardians_talk_schedule( month='June', day=16, year=2026 ) == []


def test_guardians_talk_schedule_supports_different_weekday_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time=None,
      tuesday_time=None,
      wednesday_time='13:00',
      thursday_time='14:00',
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None
   )

   wednesday_talks = GuardiansCoordinator.get_guardians_talk_schedule(
      month='June',
      day=17,
      year=2026 )
   thursday_talks = GuardiansCoordinator.get_guardians_talk_schedule(
      month='June',
      day=18,
      year=2026 )

   assert any(
      talk.name == 'African Lion' and talk.start_time == '1:00 PM'
      for talk in wednesday_talks
   )
   assert any(
      talk.name == 'African Lion' and talk.start_time == '2:00 PM'
      for talk in thursday_talks
   )


def test_guardians_talk_occurrences_cover_all_weekdays_and_cancellations(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-15',
      end_date='2026-06-21',
      monday_time='10:00',
      tuesday_time='10:00',
      wednesday_time='10:00',
      thursday_time='10:00',
      friday_time='10:00',
      saturday_time='10:00',
      sunday_time='10:00',
      message=None
   )
   assert GuardiansCoordinator.cancel_guardians_talk_occurrence(
      talk='African Lion',
      location='Africa Savanna',
      date='2026-06-18',
      time='10:00 AM'
   )

   occurrences = GuardiansCoordinator.get_guardians_talk_occurrences(
      talk='African Lion',
      location='Africa Savanna',
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
   assert GuardiansCoordinator.get_guardians_talk_occurrences( talk='', location='Africa Savanna' ) == []
   assert GuardiansCoordinator.get_guardians_talk_occurrences( talk='Bad Talk', location='Bad Location' ) == []


