from __future__ import annotations

from api_test_support.seeded_database import SeededDatabase

from api.animals.coordinators.animal_coordinator import AnimalCoordinator


def Test_GetAnimalSpeciesNames_TestSeededDatabase_ExpectReturnsSpecies(
      db: SeededDatabase ) -> None:
   assert AnimalCoordinator.get_animal_species_names()


def Test_Close_TestCalledTwice_ExpectIdempotent(
      db: SeededDatabase ) -> None:
   db.close()
   db.close()

   assert db.conn is None
