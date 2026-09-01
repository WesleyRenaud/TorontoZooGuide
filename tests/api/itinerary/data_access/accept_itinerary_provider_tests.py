from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.accept_itinerary_provider import AcceptItineraryProvider
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
   GUARDIANS_TALK       TEXT NOT NULL PRIMARY KEY,
   IS_DELETED           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryWildEncounter (
   WILD_ENCOUNTER       TEXT NOT NULL PRIMARY KEY,
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
      enclosure_name: str | None,
      old_likelihood: int,
      new_likelihood: int ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               IS_ADDED
            )
            VALUES ( ?, ?, ?, ?, ?, 0 );
      """,
      (
         species,
         exhibit,
         enclosure_name,
         old_likelihood,
         new_likelihood,
      ),
   )
   conn.commit()


def Test_AcceptItinerary_TestBelowMinLikelihoodAnimals_ExpectDeclinedRemoved(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   _insert_animal(
      accept_itinerary_conn,
      species='Spotted Hyena',
      exhibit='Africa Savanna',
      enclosure_name=None,
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
