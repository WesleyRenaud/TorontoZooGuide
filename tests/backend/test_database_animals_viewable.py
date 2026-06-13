from __future__ import annotations

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from conftest import DbControllers


def test_get_animals_viewable_on_day_returns_animals_from_seeded_database( db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_viewable_on_day( day=15, month='June', year=2026, temp=22 )

   assert animals
   assert all( animal.species for animal in animals )
   assert all( animal.likelihood > 0 for animal in animals )


def test_get_animals_viewable_on_day_filters_by_exhibit( db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      exhibits_to_include=[ 'Africa Savanna' ]
   )

   assert animals
   assert { animal.exhibit for animal in animals } == { 'Africa Savanna' }
