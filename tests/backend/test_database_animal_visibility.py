from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from conftest import DbControllers


def test_limited_viewing_and_alert_messages_are_returned(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AnimalCoordinator.set_animal_limited_viewing_schedule(
      species='African Penguin',
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      daily_start_time='09:00',
      daily_end_time='11:00',
      message='Morning viewing only.'
   )
   assert AnimalCoordinator.set_animal_viewing_alert(
      species='African Penguin',
      exhibit='Africa Savanna',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Penguins may be harder to spot.'
   )

   animals = AnimalCoordinator.get_animals_viewable_on_day( day=15, month='June', year=2026, temp=22 )
   penguin = next( animal for animal in animals if animal.species == 'African Penguin' )

   assert penguin.has_limited_viewing_schedule is True
   assert penguin.limited_viewing_message == 'Morning viewing only.'
   assert penguin.has_viewing_alert is True
   assert penguin.viewing_alert_message == 'Penguins may be harder to spot.'
