from __future__ import annotations

from collections.abc import Callable
from datetime import date

from database_console_support import get_animal

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from conftest import DbControllers


def test_set_and_remove_animal_visibility_schedule_changes_visible_animal_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AnimalCoordinator.remove_animal_visibility_schedule( 'African Lion', 'Africa Savanna' ) is False

   assert AnimalCoordinator.set_animal_limited_viewing_schedule(
      'African Lion',
      'Africa Savanna',
      '2026-06-01',
      '',
      '09:00',
      '10:00',
      ''
   )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_limited_viewing_schedule is True
   assert lion.limited_viewing_message == 'The African Lion is viewable daily only from 9:00 AM to 10:00 AM.'

   assert AnimalCoordinator.remove_animal_visibility_schedule( 'African Lion', 'Africa Savanna' ) is True

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_limited_viewing_schedule is False
   assert lion.limited_viewing_message is None
