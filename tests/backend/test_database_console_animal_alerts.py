from __future__ import annotations

from collections.abc import Callable
from datetime import date

from database_console_support import get_animal

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from conftest import DbControllers


def test_set_and_remove_animal_viewing_alert_changes_visible_animal_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_viewing_alert( 'African Lion', 'Africa Savanna', '2026-06-01', '', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_viewing_alert is True
   assert lion.viewing_alert_messages == [
      'The African Lion may be less visible than usual at this time.',
   ]

   assert AnimalCoordinator.remove_animal_viewing_alert( 'African Lion', 'Africa Savanna' ) is True

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_viewing_alert is False
   assert lion.viewing_alert_messages == []
