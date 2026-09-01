from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.accept_itinerary_provider import AcceptItineraryProvider
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.shared.constants import Constants


ACCEPT_ITINERARY_SCHEMA = """
CREATE TABLE ItineraryAnimal (
   SPECIES              TEXT NOT NULL,
   EXHIBIT              TEXT NOT NULL,
   ENCLOSURE_NAME       TEXT,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   IS_ADDED             INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryAttraction (
   ATTRACTION           TEXT NOT NULL PRIMARY KEY,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER
);

CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER NOT NULL DEFAULT 0,
   OLD_LIKELIHOOD           INTEGER,
   NEW_LIKELIHOOD           INTEGER
);

CREATE TABLE ItineraryGuardiansTalk (
   TALK_NAME            TEXT NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryWildEncounter (
   WILD_ENCOUNTER       TEXT NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER NOT NULL DEFAULT 0
);
"""


@pytest.fixture
def accept_itinerary_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ACCEPT_ITINERARY_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


def _insert_animal(
      conn: sqlite3.Connection,
      *,
      species: str,
      exhibit: str,
      old_likelihood: int,
      new_likelihood: int,
      enclosure_name: str | None = None,
      is_added: int = 0 ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               IS_ADDED
            )
            VALUES ( ?, ?, ?, ?, ?, ? );
      """,
      (
         species,
         exhibit,
         enclosure_name,
         old_likelihood,
         new_likelihood,
         is_added,
      ),
   )
   conn.commit()


def _insert_attraction(
      conn: sqlite3.Connection,
      *,
      attraction: str,
      old_likelihood: int,
      new_likelihood: int ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES ( ?, ?, ? );
      """,
      ( attraction, old_likelihood, new_likelihood ),
   )
   conn.commit()


def Test_AcceptItinerary_TestAddedAnimalFlags_ExpectCleared(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   _insert_animal(
      accept_itinerary_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=90,
      new_likelihood=90,
      is_added=1 )
   _insert_animal(
      accept_itinerary_conn,
      species='African Penguin',
      exhibit='Africa Savanna',
      old_likelihood=80,
      new_likelihood=80 )

   assert AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn ) is True

   assert accept_itinerary_conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal WHERE IS_ADDED = 1;'
   ).fetchone()[ 0 ] == 0
   assert accept_itinerary_conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal WHERE OLD_LIKELIHOOD IS NOT NULL;'
   ).fetchone()[ 0 ] == 0


def Test_AcceptItinerary_TestZeroLikelihoodAndDeletedItems_ExpectDeclinedRemoved(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   _insert_animal(
      accept_itinerary_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=90,
      new_likelihood=60 )
   _insert_animal(
      accept_itinerary_conn,
      species='African Penguin',
      exhibit='Africa Savanna',
      old_likelihood=40,
      new_likelihood=80 )
   _insert_attraction(
      accept_itinerary_conn,
      attraction='Conservation Carousel',
      old_likelihood=100,
      new_likelihood=0 )
   _insert_attraction(
      accept_itinerary_conn,
      attraction='Greenhouse',
      old_likelihood=50,
      new_likelihood=75 )
   accept_itinerary_conn.executemany(
      """   INSERT INTO ItineraryGuardiansTalk (
               TALK_NAME,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, ? );
      """,
      [
         ( 'African Lion', '10:00 AM', '10:30 AM', 1 ),
         ( 'Amur Tiger', '11:00', '11:30', 0 ),
      ],
   )
   accept_itinerary_conn.executemany(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, ? );
      """,
      [
         ( 'African Rainforest', '2:00 PM', '2:45 PM', 1 ),
         ( 'Kangaroo', '1:00 PM', '1:45 PM', 0 ),
      ],
   )
   accept_itinerary_conn.commit()

   assert AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn ) is True

   assert [
      row[ 'SPECIES' ]
      for row in accept_itinerary_conn.execute( 'SELECT SPECIES FROM ItineraryAnimal;' )
   ] == [ 'African Lion', 'African Penguin' ]
   assert [
      row[ 'ATTRACTION' ]
      for row in accept_itinerary_conn.execute( 'SELECT ATTRACTION FROM ItineraryAttraction;' )
   ] == [ 'Greenhouse' ]
   assert [
      row[ 'TALK_NAME' ]
      for row in accept_itinerary_conn.execute( 'SELECT TALK_NAME FROM ItineraryGuardiansTalk;' )
   ] == [ 'Amur Tiger' ]
   assert [
      row[ 'WILD_ENCOUNTER' ]
      for row in accept_itinerary_conn.execute(
         'SELECT WILD_ENCOUNTER FROM ItineraryWildEncounter;' )
   ] == [ 'Kangaroo' ]


def Test_AcceptItinerary_TestBelowMinLikelihoodAnimals_ExpectDeclinedRemoved(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   _insert_animal(
      accept_itinerary_conn,
      species='Spotted Hyena',
      exhibit='Africa Savanna',
      old_likelihood=80,
      new_likelihood=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD - 1 )
   _insert_animal(
      accept_itinerary_conn,
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Giraffe House',
      old_likelihood=80,
      new_likelihood=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD )

   assert AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn ) is True

   remaining_species = {
      row[ 'SPECIES' ]
      for row in accept_itinerary_conn.execute( 'SELECT SPECIES FROM ItineraryAnimal;' )
   }
   assert remaining_species == { 'Masai Giraffe' }


def Test_AcceptItinerary_TestBelowMinLikelihoodWithoutOverride_ExpectThresholdSplit(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   _insert_animal(
      accept_itinerary_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=80,
      new_likelihood=0 )
   _insert_animal(
      accept_itinerary_conn,
      species='Spotted Hyena',
      exhibit='Africa Savanna',
      old_likelihood=70,
      new_likelihood=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD - 1 )
   _insert_animal(
      accept_itinerary_conn,
      species='African Penguin',
      exhibit='Africa Savanna',
      old_likelihood=90,
      new_likelihood=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD )

   assert AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn ) is True

   assert [
      row[ 'SPECIES' ]
      for row in accept_itinerary_conn.execute(
         'SELECT SPECIES FROM ItineraryAnimal ORDER BY SPECIES;' )
   ] == [ 'African Penguin' ]


def Test_AcceptItinerary_TestZeroLikelihoodAnimals_ExpectAllRemoved(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   _insert_animal(
      accept_itinerary_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=80,
      new_likelihood=0 )
   _insert_animal(
      accept_itinerary_conn,
      species='African Penguin',
      exhibit='Africa Savanna',
      old_likelihood=70,
      new_likelihood=0 )

   assert AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn ) is True

   assert accept_itinerary_conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal;'
   ).fetchone()[ 0 ] == 0


def Test_AcceptItinerary_TestZeroLikelihoodAnimalsWithOverride_ExpectKeptAnimal(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   _insert_animal(
      accept_itinerary_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=80,
      new_likelihood=0 )
   _insert_animal(
      accept_itinerary_conn,
      species='African Penguin',
      exhibit='Africa Savanna',
      old_likelihood=70,
      new_likelihood=0 )

   assert AcceptItineraryProvider.accept_itinerary(
      accept_itinerary_conn,
      animals_to_keep=[
         ItineraryAnimalInput(
            species='African Lion',
            exhibit='Africa Savanna' ),
      ] ) is True

   rows = accept_itinerary_conn.execute(
      """   SELECT SPECIES, EXHIBIT, OLD_LIKELIHOOD
            FROM ItineraryAnimal
            ORDER BY SPECIES;
      """
   ).fetchall()

   assert len( rows ) == 1
   assert rows[ 0 ][ 'SPECIES' ] == 'African Lion'
   assert rows[ 0 ][ 'EXHIBIT' ] == 'Africa Savanna'
   assert rows[ 0 ][ 'OLD_LIKELIHOOD' ] is None


def Test_AcceptItinerary_TestZeroLikelihoodAttractions_ExpectAllRemoved(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   _insert_attraction(
      accept_itinerary_conn,
      attraction='Conservation Carousel',
      old_likelihood=100,
      new_likelihood=0 )
   _insert_attraction(
      accept_itinerary_conn,
      attraction='Greenhouse',
      old_likelihood=80,
      new_likelihood=0 )

   assert AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn ) is True

   assert accept_itinerary_conn.execute(
      'SELECT COUNT(*) FROM ItineraryAttraction;'
   ).fetchone()[ 0 ] == 0


def Test_AcceptItinerary_TestZeroLikelihoodAttractionsWithOverride_ExpectKeptAttraction(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   _insert_attraction(
      accept_itinerary_conn,
      attraction='Conservation Carousel',
      old_likelihood=100,
      new_likelihood=0 )
   _insert_attraction(
      accept_itinerary_conn,
      attraction='Greenhouse',
      old_likelihood=80,
      new_likelihood=0 )

   assert AcceptItineraryProvider.accept_itinerary(
      accept_itinerary_conn,
      attractions_to_keep=[ 'Conservation Carousel' ] ) is True

   rows = accept_itinerary_conn.execute(
      """   SELECT ATTRACTION, OLD_LIKELIHOOD
            FROM ItineraryAttraction
            ORDER BY ATTRACTION;
      """
   ).fetchall()

   assert len( rows ) == 1
   assert rows[ 0 ][ 'ATTRACTION' ] == 'Conservation Carousel'
   assert rows[ 0 ][ 'OLD_LIKELIHOOD' ] is None
