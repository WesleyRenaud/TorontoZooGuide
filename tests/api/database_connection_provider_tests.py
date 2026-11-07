from __future__ import annotations

from pathlib import Path
import sqlite3

from api_test_support.seeded_database import SeededDatabase
import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.database_connection_provider import DatabaseConnectionProvider


def Test_GetAnimalSpeciesNames_TestSeededDatabase_ExpectReturnsSpecies(
      db: SeededDatabase ) -> None:
   species_names = AnimalCoordinator.get_animal_species_names()

   assert species_names


def Test_Close_TestCalledTwice_ExpectIdempotent(
      db: SeededDatabase ) -> None:
   db.close()
   db.close()

   assert db.conn is None


def Test_OpenReadOnly_TestSeededDatabase_ExpectReadSucceedsAndWriteFails(
      db_path: Path ) -> None:
   connection = DatabaseConnectionProvider.open_read_only( db_path )
   row = connection.execute( 'SELECT 1' ).fetchone()

   with pytest.raises( sqlite3.OperationalError ):
      connection.execute( 'CREATE TABLE ReadOnlyProbe ( ID INTEGER )' )

   DatabaseConnectionProvider.close( connection )

   assert row[ 0 ] == 1
