from __future__ import annotations

from collections.abc import Callable
from datetime import date

from database_console_support import get_animal

from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from conftest import DbControllers


def test_set_exhibit_closed_and_open_changes_animal_and_closed_exhibit_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ExhibitCoordinator.set_exhibit_as_closed( 'Africa Savanna', '2026-06-01', '2026-06-30', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood == 0
   assert lion.off_display_message == 'The Africa Savanna is temporarily closed.'
   assert 'Africa Savanna' in ExhibitCoordinator.get_closed_exhibits_for_visit_date( month='June', day=15, year=2026 )

   assert ExhibitCoordinator.set_exhibit_as_open( 'Africa Savanna', '2026-06-01', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood > 0
   assert lion.off_display_message is None
   assert 'Africa Savanna' not in ExhibitCoordinator.get_closed_exhibits_for_visit_date( month='June', day=15, year=2026 )
