from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.models import Update
from api.updates.coordinators.update_coordinator import UpdateCoordinator
from api.updates.domain.update_sort import sort_updates_for_display
from api.updates.domain.update_type import UpdateType
from conftest import DbControllers


def test_update_type_display_order() -> None:
   assert UpdateType.CLOSURE.order == 0
   assert UpdateType.ANIMAL_BIRTH.order == 1
   assert UpdateType.ANIMAL_PASSING.order == 2
   assert UpdateType.NEW_ARRIVAL.order == 3
   assert UpdateType.DEPARTURE.order == 4


def test_sort_updates_for_display_groups_by_type_then_sooner_end_date() -> None:
   updates = [
      Update(
         title='Open-ended departure',
         description='',
         update_type='Departure',
         start_date='2026-01-01',
         end_date=None ),
      Update(
         title='Later birth',
         description='',
         update_type='Animal Birth',
         start_date='2026-01-01',
         end_date='2026-08-01' ),
      Update(
         title='Sooner birth',
         description='',
         update_type='Animal Birth',
         start_date='2026-01-01',
         end_date='2026-07-01' ),
      Update(
         title='Closure A',
         description='',
         update_type='Closure',
         start_date='2026-01-01',
         end_date='2026-09-01' ),
      Update(
         title='Closure B',
         description='',
         update_type='Closure',
         start_date='2026-01-01',
         end_date='2026-06-01' ),
      Update(
         title='Passing',
         description='',
         update_type='Animal Passing',
         start_date='2026-01-01',
         end_date='2026-07-15' ),
      Update(
         title='Arrival',
         description='',
         update_type='New Arrival',
         start_date='2026-01-01',
         end_date='2026-07-15' ),
      Update(
         title='Ending departure',
         description='',
         update_type='Departure',
         start_date='2026-01-01',
         end_date='2026-07-01' ),
   ]

   assert [ update.title for update in sort_updates_for_display( updates ) ] == [
      'Closure B',
      'Closure A',
      'Sooner birth',
      'Later birth',
      'Passing',
      'Arrival',
      'Ending departure',
      'Open-ended departure',
   ]


def test_get_updates_for_visit_date_returns_type_then_end_date_order(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert UpdateCoordinator.create_update(
      title='Later closure',
      description='Ends later.',
      update_type='Closure',
      start_date='2026-06-01',
      end_date='2026-08-01' )
   assert UpdateCoordinator.create_update(
      title='Sooner birth',
      description='Ends sooner.',
      update_type='Animal Birth',
      start_date='2026-06-01',
      end_date='2026-07-01' )
   assert UpdateCoordinator.create_update(
      title='Sooner closure',
      description='Ends sooner.',
      update_type='Closure',
      start_date='2026-06-01',
      end_date='2026-07-01' )
   assert UpdateCoordinator.create_update(
      title='Open arrival',
      description='No end date.',
      update_type='New Arrival',
      start_date='2026-06-01',
      end_date=None )

   updates = UpdateCoordinator.get_updates_for_visit_date(
      month='June',
      day=15,
      year=2026 )

   assert [ update.title for update in updates ] == [
      'Sooner closure',
      'Later closure',
      'Sooner birth',
      'Open arrival',
   ]
