from __future__ import annotations

from datetime import date

from api_test_support.frozen_datetime import patch_database_today
from api_test_support.seeded_database import SeededDatabase
import pytest

from api.updates.coordinators.update_coordinator import UpdateCoordinator


UPDATE_TITLE = 'New baby giraffe'
UPDATE_DESCRIPTION = 'Come meet the new calf.'
UPDATE_TYPE = 'new arrival'
UPDATE_START_DATE = '2026-06-15'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026


def Test_CreateUpdate_TestBlankStartDate_ExpectUsesToday(
      db: SeededDatabase,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   patch_database_today( monkeypatch, date( 2026, 6, 15 ) )

   assert UpdateCoordinator.create_update(
      title='Zoomobile update',
      description='Route change today.',
      update_type='Closure',
      start_date='',
      end_date=None )

   updates = UpdateCoordinator.get_updates_for_visit_date(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR )

   assert len( updates ) == 1
   assert updates[ 0 ].start_date == '2026-06-15'


def Test_CreateEndAndEditUpdate_TestLifecycle_ExpectActiveUpdateResultsChange(
      db: SeededDatabase,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   patch_database_today( monkeypatch, date( 2026, 6, 15 ) )

   created = UpdateCoordinator.create_update(
      title=UPDATE_TITLE,
      description=UPDATE_DESCRIPTION,
      update_type=UPDATE_TYPE,
      start_date=UPDATE_START_DATE,
      end_date=None )

   assert created is True

   updates = UpdateCoordinator.get_updates_for_visit_date(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR )

   assert len( updates ) == 1
   assert updates[ 0 ].to_dict() == {
      'title': UPDATE_TITLE,
      'description': UPDATE_DESCRIPTION,
      'type': 'New Arrival',
      'start_date': UPDATE_START_DATE,
      'end_date': None,
   }

   assert UpdateCoordinator.edit_update(
      title=UPDATE_TITLE,
      start_date=UPDATE_START_DATE,
      description='Updated calf details.',
      update_type='Closure',
      end_date='2026-07-15' ) is True

   updates = UpdateCoordinator.get_updates_for_visit_date( month='July', day=1, year=2026 )

   assert len( updates ) == 1
   assert updates[ 0 ].to_dict() == {
      'title': UPDATE_TITLE,
      'description': 'Updated calf details.',
      'type': 'Closure',
      'start_date': UPDATE_START_DATE,
      'end_date': '2026-07-15',
   }

   assert UpdateCoordinator.edit_update(
      title=UPDATE_TITLE,
      start_date=UPDATE_START_DATE,
      description='Updated calf details.',
      update_type='Closure',
      end_date=None ) is True

   updates = UpdateCoordinator.get_updates_for_visit_date( month='August', day=1, year=2026 )

   assert updates[ 0 ].end_date is None

   assert UpdateCoordinator.end_update( UPDATE_TITLE, UPDATE_START_DATE, '2026-06-14' ) is True
   assert UpdateCoordinator.get_updates_for_visit_date(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == []


def Test_GetUnexpiredUpdates_TestFutureAndExpiredUpdates_ExpectFutureOnly(
      db: SeededDatabase,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   patch_database_today( monkeypatch, date( 2026, 6, 15 ) )

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

   assert UpdateCoordinator.get_updates_for_visit_date(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == []

   update_options = UpdateCoordinator.get_unexpired_updates()

   assert [ update.title for update in update_options ] == [ 'Future update' ]


def Test_CreateUpdate_TestConsoleStatusTypes_ExpectPersistAnimalBirthAndPassing(
      db: SeededDatabase ) -> None:
   assert UpdateCoordinator.create_update(
      'Animal birth',
      'A new animal was born.',
      'animal birth',
      '2026-06-01',
      '2026-06-30',
   ) is True
   assert UpdateCoordinator.create_update(
      'Animal passing',
      'An animal has passed.',
      'animal_passing',
      '2026-06-01',
      '2026-06-30',
   ) is True
