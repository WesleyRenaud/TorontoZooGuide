from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.updates.coordinators.update_coordinator import UpdateCoordinator
from conftest import DbControllers

def test_create_update_uses_today_when_start_date_is_blank(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert UpdateCoordinator.create_update(
      title='Zoomobile update',
      description='Route change today.',
      update_type='Closure',
      start_date='',
      end_date=None )

   updates = UpdateCoordinator.get_updates_for_visit_date( month='June', day=15, year=2026 )

   assert len( updates ) == 1
   assert updates[ 0 ].start_date == '2026-06-15'

def test_create_end_and_edit_updates_change_active_update_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   created = UpdateCoordinator.create_update(
      title='New baby giraffe',
      description='Come meet the new calf.',
      update_type='new arrival',
      start_date='2026-06-15',
      end_date=None )

   assert created is True

   updates = UpdateCoordinator.get_updates_for_visit_date( month='June', day=15, year=2026 )

   assert len( updates ) == 1
   assert updates[ 0 ].to_dict() == {
      'title': 'New baby giraffe',
      'description': 'Come meet the new calf.',
      'type': 'New Arrival',
      'start_date': '2026-06-15',
      'end_date': None
   }

   assert UpdateCoordinator.edit_update(
      title='New baby giraffe',
      start_date='2026-06-15',
      description='Updated calf details.',
      update_type='Closure',
      end_date='2026-07-15' ) is True

   updates = UpdateCoordinator.get_updates_for_visit_date( month='July', day=1, year=2026 )

   assert len( updates ) == 1
   assert updates[ 0 ].to_dict() == {
      'title': 'New baby giraffe',
      'description': 'Updated calf details.',
      'type': 'Closure',
      'start_date': '2026-06-15',
      'end_date': '2026-07-15'
   }

   assert UpdateCoordinator.edit_update(
      title='New baby giraffe',
      start_date='2026-06-15',
      description='Updated calf details.',
      update_type='Closure',
      end_date=None ) is True

   updates = UpdateCoordinator.get_updates_for_visit_date( month='August', day=1, year=2026 )

   assert updates[ 0 ].end_date is None

   assert UpdateCoordinator.end_update( 'New baby giraffe', '2026-06-15', '2026-06-14' ) is True
   assert UpdateCoordinator.get_updates_for_visit_date( month='June', day=15, year=2026 ) == []

def test_active_update_options_include_future_updates_but_not_expired_updates(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert UpdateCoordinator.create_update(
      title='Future update',
      description='This starts later.',
      update_type='Closure',
      start_date='2026-07-01',
      end_date='2026-07-31' )

   assert UpdateCoordinator.create_update(
      title='Expired update',
      description='This already ended.',
      update_type='Closure',
      start_date='2026-05-01',
      end_date='2026-05-31' )

   assert UpdateCoordinator.get_updates_for_visit_date( month='June', day=15, year=2026 ) == []

   update_options = UpdateCoordinator.get_unexpired_updates()

   assert [ update.title for update in update_options ] == [ 'Future update' ]

def test_console_status_and_schedule_guards( db: DbControllers ) -> None:
   assert UpdateCoordinator.create_update(
      'Animal birth',
      'A new animal was born.',
      'animal birth',
      '2026-06-01',
      '2026-06-30'
   ) is True
   assert UpdateCoordinator.create_update(
      'Animal passing',
      'An animal has passed.',
      'animal_passing',
      '2026-06-01',
      '2026-06-30'
   ) is True
