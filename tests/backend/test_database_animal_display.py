from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from conftest import DbControllers


def test_off_display_animals_are_excluded_or_included_by_flag(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   AnimalCoordinator.set_animal_as_off_display(
      species='African Lion',
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Lions are resting.'
   )

   without_closed = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=False
   )
   with_closed = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   assert all( animal.species != 'African Lion' for animal in without_closed )
   lion = next( animal for animal in with_closed if animal.species == 'African Lion' )
   assert lion.likelihood == 0
   assert lion.off_display_message == 'Lions are resting.'


def test_exhibit_closure_sets_animal_likelihood_to_zero(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   ExhibitCoordinator.set_exhibit_as_closed(
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Savanna is closed.'
   )

   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True,
      exhibits_to_include=[ 'Africa Savanna' ]
   )

   assert animals
   assert all( animal.likelihood == 0 for animal in animals )
   assert all( animal.off_display_message == 'Savanna is closed.' for animal in animals )
