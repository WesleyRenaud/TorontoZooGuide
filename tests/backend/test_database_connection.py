from __future__ import annotations

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from conftest import DbControllers


def test_database_uses_injected_path( db: DbControllers ) -> None:
   assert AnimalCoordinator.get_animal_species_names()


def test_close_is_idempotent( db: DbControllers ) -> None:
   db.close()
   db.close()

   assert db.conn is None
