from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.types import Cursor
from conftest import DbControllers


def test_setting_animal_viewing_alert_twice_updates_existing_alert(
      db: DbControllers,
      cursor: Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AnimalCoordinator.set_animal_viewing_alert(
      species='African Penguin',
      exhibit='Africa Savanna',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Penguins may be harder to spot.'
   )
   assert AnimalCoordinator.set_animal_viewing_alert(
      species='African Penguin',
      exhibit='Africa Savanna',
      alert_start_date='2026-06-15',
      alert_end_date='2026-07-15',
      message='Penguin viewing has moved.'
   )

   alert_rows = cursor.execute(
      """ SELECT
             ALERT_MESSAGE,
             ALERT_START_DATE,
             ALERT_END_DATE
          FROM AnimalViewingAlert
          WHERE SPECIES = ?
          AND EXHIBIT = ?;
      """,
      ( 'African Penguin', 'Africa Savanna' )
   ).fetchall()
   animals = AnimalCoordinator.get_animals_viewable_on_day( day=15, month='June', year=2026, temp=22 )
   penguin = next( animal for animal in animals if animal.species == 'African Penguin' )

   assert len( alert_rows ) == 1
   assert dict( alert_rows[ 0 ] ) == {
      'ALERT_MESSAGE': 'Penguin viewing has moved.',
      'ALERT_START_DATE': '2026-06-15',
      'ALERT_END_DATE': '2026-07-15'
   }
   assert penguin.has_viewing_alert is True
   assert penguin.viewing_alert_messages == [ 'Penguin viewing has moved.' ]
