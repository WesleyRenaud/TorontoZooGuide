from __future__ import annotations

from pathlib import Path
import sqlite3

from api_test_support.seeded_database import SeededDatabase
import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.database_connection_provider import DatabaseConnectionProvider
from api.shared.enums.position import Position


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


def Test_Open_TestAnimalsPath_ExpectItineraryAttached(
      tmp_path: Path ) -> None:
   animals_path = tmp_path / 'animals.db'
   sqlite3.connect( animals_path ).close()

   connection = DatabaseConnectionProvider.open( str( animals_path ) )
   schemas = {
      row[ Position.SECOND ]
      for row in connection.execute( 'PRAGMA database_list;' )
   }
   itinerary_tables = {
      row[ Position.FIRST ]
      for row in connection.execute(
         "SELECT name FROM itinerary.sqlite_master WHERE type = 'table'"
      )
   }
   DatabaseConnectionProvider.close( connection )

   assert DatabaseConnectionProvider.ITINERARY_SCHEMA in schemas
   assert 'ItineraryDate' in itinerary_tables
   assert DatabaseConnectionProvider.itinerary_path_beside( animals_path ).is_file()


def Test_Open_TestWriteItinerary_ExpectNotStoredOnAnimalsMain(
      tmp_path: Path ) -> None:
   animals_path = tmp_path / 'animals.db'
   exhibit = 'Africa Savanna'
   sqlite3.connect( animals_path ).close()

   conn = DatabaseConnectionProvider.open( str( animals_path ) )
   conn.execute(
      'INSERT INTO ItineraryExhibit ( EXHIBIT ) VALUES ( ? )',
      ( exhibit, ),
   )
   conn.commit()
   exhibit_count = conn.execute(
      'SELECT COUNT(*) FROM ItineraryExhibit WHERE EXHIBIT = ?',
      ( exhibit, ),
   ).fetchone()[ Position.FIRST ]
   main_tables = {
      row[ Position.FIRST ]
      for row in conn.execute(
         "SELECT name FROM main.sqlite_master WHERE type = 'table'"
      )
   }
   DatabaseConnectionProvider.close( conn )

   assert exhibit_count == 1
   assert 'ItineraryExhibit' not in main_tables


def Test_AttachItinerary_TestMemoryDatabase_ExpectNoOp() -> None:
   conn = sqlite3.connect( ':memory:' )

   DatabaseConnectionProvider.attach_itinerary( conn, ':memory:' )
   schemas = {
      row[ Position.SECOND ]
      for row in conn.execute( 'PRAGMA database_list;' )
   }
   DatabaseConnectionProvider.close( conn )

   assert schemas == { 'main' }


def Test_AttachItinerary_TestAlreadyAttached_ExpectIdempotent(
      tmp_path: Path ) -> None:
   animals_path = tmp_path / 'animals.db'
   animals_path_text = str( animals_path )
   conn = DatabaseConnectionProvider.open( animals_path_text )

   DatabaseConnectionProvider.attach_itinerary( conn, animals_path_text )
   schemas = {
      row[ Position.SECOND ]
      for row in conn.execute( 'PRAGMA database_list;' )
   }
   DatabaseConnectionProvider.close( conn )

   assert DatabaseConnectionProvider.ITINERARY_SCHEMA in schemas
