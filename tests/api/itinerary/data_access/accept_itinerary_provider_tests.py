from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.accept_itinerary_provider import AcceptItineraryProvider
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.shared.constants import Constants
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


ACCEPT_ITINERARY_SCHEMA = """
CREATE TABLE ItineraryAnimal (
   SPECIES                 TEXT NOT NULL,
   EXHIBIT                 TEXT NOT NULL,
   ENCLOSURE_NAME          TEXT,
   OLD_LIKELIHOOD          INTEGER,
   NEW_LIKELIHOOD          INTEGER,
   IS_ADDED                INTEGER NOT NULL DEFAULT 0,
   COVERED_BY_TALK         INTEGER NOT NULL DEFAULT 0,
   ADDED_BY_TRANSPORTATION INTEGER NOT NULL DEFAULT 0,
   START_TIME              TEXT,
   END_TIME                TEXT
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

CREATE TABLE ItineraryTransportationLeg (
   TRANSPORTATION           TEXT NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER NOT NULL DEFAULT 0,
   FROM_STATION             TEXT NOT NULL,
   TO_STATION               TEXT NOT NULL,
   START_TIME               TEXT NOT NULL,
   END_TIME                 TEXT NOT NULL
);

CREATE TABLE ItineraryTransportationRouteMarker (
   TRANSPORTATION           TEXT NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER NOT NULL DEFAULT 0,
   SEQUENCE                 INTEGER NOT NULL,
   MARKER_ORDER             INTEGER NOT NULL,
   MARKER_ID                TEXT NOT NULL
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

CREATE TABLE TransportationAnimal (
   TRANSPORTATION      TEXT        NOT NULL,
   FROM_STATION        TEXT        NOT NULL,
   TO_STATION          TEXT        NOT NULL,
   SPECIES             TEXT        NOT NULL,
   EXHIBIT             TEXT        NOT NULL,
   ENCLOSURE_NAME      TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT, ENCLOSURE_NAME )
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


def _insert_transportation(
      conn: sqlite3.Connection,
      *,
      transportation: str,
      added_as_attraction: int,
      old_likelihood: int,
      new_likelihood: int ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES ( ?, ?, ?, ? );
      """,
      ( transportation, added_as_attraction, old_likelihood, new_likelihood ),
   )
   conn.commit()


def Test_AcceptItinerary_TestAddedAnimalFlags_ExpectCleared(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   lion_species = 'African Lion'
   penguin_species = 'African Penguin'
   exhibit = 'Africa Savanna'
   _insert_animal(
      accept_itinerary_conn,
      species=lion_species,
      exhibit=exhibit,
      old_likelihood=90,
      new_likelihood=90,
      is_added=1 )
   _insert_animal(
      accept_itinerary_conn,
      species=penguin_species,
      exhibit=exhibit,
      old_likelihood=80,
      new_likelihood=80 )

   accepted = AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn )
   added_count = accept_itinerary_conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal WHERE IS_ADDED = 1;'
   ).fetchone()[ Position.FIRST ]
   old_likelihood_count = accept_itinerary_conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal WHERE OLD_LIKELIHOOD IS NOT NULL;'
   ).fetchone()[ Position.FIRST ]

   assert accepted is True
   assert added_count == 0
   assert old_likelihood_count == 0


def Test_AcceptItinerary_TestZeroLikelihoodAndDeletedItems_ExpectDeclinedRemoved(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   lion_species = 'African Lion'
   penguin_species = 'African Penguin'
   exhibit = 'Africa Savanna'
   carousel = 'Conservation Carousel'
   greenhouse = 'Greenhouse'
   deleted_talk = 'African Lion'
   kept_talk = 'Amur Tiger'
   talk_start_time = '10:00 AM'
   talk_duration_minutes = 30
   kept_talk_start_time = '11:00'
   kept_talk_duration_minutes = 30
   deleted_encounter = 'African Rainforest'
   kept_encounter = 'Kangaroo'
   encounter_start_time = '2:00 PM'
   encounter_duration_minutes = 45
   kept_encounter_start_time = '1:00 PM'
   kept_encounter_duration_minutes = 45
   _insert_animal(
      accept_itinerary_conn,
      species=lion_species,
      exhibit=exhibit,
      old_likelihood=90,
      new_likelihood=60 )
   _insert_animal(
      accept_itinerary_conn,
      species=penguin_species,
      exhibit=exhibit,
      old_likelihood=40,
      new_likelihood=80 )
   _insert_attraction(
      accept_itinerary_conn,
      attraction=carousel,
      old_likelihood=100,
      new_likelihood=0 )
   _insert_attraction(
      accept_itinerary_conn,
      attraction=greenhouse,
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
         (
            deleted_talk,
            talk_start_time,
            DateValues.add_minutes_to_time( talk_start_time, talk_duration_minutes ),
            1,
         ),
         (
            kept_talk,
            kept_talk_start_time,
            DateValues.add_minutes_to_time(
               kept_talk_start_time,
               kept_talk_duration_minutes ),
            0,
         ),
      ] )
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
         (
            deleted_encounter,
            encounter_start_time,
            DateValues.add_minutes_to_time(
               encounter_start_time,
               encounter_duration_minutes ),
            1,
         ),
         (
            kept_encounter,
            kept_encounter_start_time,
            DateValues.add_minutes_to_time(
               kept_encounter_start_time,
               kept_encounter_duration_minutes ),
            0,
         ),
      ] )
   accept_itinerary_conn.commit()

   accepted = AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn )
   animal_names = [
      row[ 'SPECIES' ]
      for row in accept_itinerary_conn.execute( 'SELECT SPECIES FROM ItineraryAnimal;' )
   ]
   attraction_names = [
      row[ 'ATTRACTION' ]
      for row in accept_itinerary_conn.execute( 'SELECT ATTRACTION FROM ItineraryAttraction;' )
   ]
   talk_names = [
      row[ 'TALK_NAME' ]
      for row in accept_itinerary_conn.execute( 'SELECT TALK_NAME FROM ItineraryGuardiansTalk;' )
   ]
   encounter_names = [
      row[ 'WILD_ENCOUNTER' ]
      for row in accept_itinerary_conn.execute(
         'SELECT WILD_ENCOUNTER FROM ItineraryWildEncounter;' )
   ]

   assert accepted is True
   assert animal_names == [ lion_species, penguin_species ]
   assert attraction_names == [ greenhouse ]
   assert talk_names == [ kept_talk ]
   assert encounter_names == [ kept_encounter ]


def Test_AcceptItinerary_TestBelowMinLikelihoodAnimals_ExpectDeclinedRemoved(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   declined_species = 'Spotted Hyena'
   kept_species = 'Masai Giraffe'
   exhibit = 'Africa Savanna'
   enclosure_name = 'Giraffe House'
   _insert_animal(
      accept_itinerary_conn,
      species=declined_species,
      exhibit=exhibit,
      old_likelihood=80,
      new_likelihood=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD - 1 )
   _insert_animal(
      accept_itinerary_conn,
      species=kept_species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      old_likelihood=80,
      new_likelihood=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD )

   accepted = AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn )
   remaining_species = {
      row[ 'SPECIES' ]
      for row in accept_itinerary_conn.execute( 'SELECT SPECIES FROM ItineraryAnimal;' )
   }

   assert accepted is True
   assert remaining_species == { kept_species }


def Test_AcceptItinerary_TestBelowMinLikelihoodWithoutOverride_ExpectThresholdSplit(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   lion_species = 'African Lion'
   hyena_species = 'Spotted Hyena'
   penguin_species = 'African Penguin'
   exhibit = 'Africa Savanna'
   _insert_animal(
      accept_itinerary_conn,
      species=lion_species,
      exhibit=exhibit,
      old_likelihood=80,
      new_likelihood=0 )
   _insert_animal(
      accept_itinerary_conn,
      species=hyena_species,
      exhibit=exhibit,
      old_likelihood=70,
      new_likelihood=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD - 1 )
   _insert_animal(
      accept_itinerary_conn,
      species=penguin_species,
      exhibit=exhibit,
      old_likelihood=90,
      new_likelihood=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD )

   accepted = AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn )
   remaining_species = [
      row[ 'SPECIES' ]
      for row in accept_itinerary_conn.execute(
         'SELECT SPECIES FROM ItineraryAnimal ORDER BY SPECIES;' )
   ]

   assert accepted is True
   assert remaining_species == [ penguin_species ]


def Test_AcceptItinerary_TestZeroLikelihoodAnimals_ExpectAllRemoved(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   exhibit = 'Africa Savanna'
   _insert_animal(
      accept_itinerary_conn,
      species='African Lion',
      exhibit=exhibit,
      old_likelihood=80,
      new_likelihood=0 )
   _insert_animal(
      accept_itinerary_conn,
      species='African Penguin',
      exhibit=exhibit,
      old_likelihood=70,
      new_likelihood=0 )

   accepted = AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn )
   remaining_count = accept_itinerary_conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal;'
   ).fetchone()[ Position.FIRST ]

   assert accepted is True
   assert remaining_count == 0


def Test_AcceptItinerary_TestZeroLikelihoodAnimalsWithOverride_ExpectKeptAnimal(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   animals_to_keep = [
      ItineraryAnimalInput(
         species=species,
         exhibit=exhibit ),
   ]
   _insert_animal(
      accept_itinerary_conn,
      species=species,
      exhibit=exhibit,
      old_likelihood=80,
      new_likelihood=0 )
   _insert_animal(
      accept_itinerary_conn,
      species='African Penguin',
      exhibit=exhibit,
      old_likelihood=70,
      new_likelihood=0 )

   accepted = AcceptItineraryProvider.accept_itinerary(
      accept_itinerary_conn,
      animals_to_keep=animals_to_keep )
   rows = accept_itinerary_conn.execute(
      """   SELECT SPECIES, EXHIBIT, OLD_LIKELIHOOD
            FROM ItineraryAnimal
            ORDER BY SPECIES;
      """
   ).fetchall()

   kept_animal = animals_to_keep[ Position.FIRST ]
   assert accepted is True
   assert len( rows ) == len( animals_to_keep )
   assert rows[ Position.FIRST ][ 'SPECIES' ] == kept_animal.species
   assert rows[ Position.FIRST ][ 'EXHIBIT' ] == kept_animal.exhibit
   assert rows[ Position.FIRST ][ 'OLD_LIKELIHOOD' ] is None


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

   accepted = AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn )
   remaining_count = accept_itinerary_conn.execute(
      'SELECT COUNT(*) FROM ItineraryAttraction;'
   ).fetchone()[ Position.FIRST ]

   assert accepted is True
   assert remaining_count == 0


def Test_AcceptItinerary_TestZeroLikelihoodAttractionsWithOverride_ExpectKeptAttraction(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   kept_attraction = 'Conservation Carousel'
   attractions_to_keep = [ kept_attraction ]
   _insert_attraction(
      accept_itinerary_conn,
      attraction=kept_attraction,
      old_likelihood=100,
      new_likelihood=0 )
   _insert_attraction(
      accept_itinerary_conn,
      attraction='Greenhouse',
      old_likelihood=80,
      new_likelihood=0 )

   accepted = AcceptItineraryProvider.accept_itinerary(
      accept_itinerary_conn,
      attractions_to_keep=attractions_to_keep )
   rows = accept_itinerary_conn.execute(
      """   SELECT ATTRACTION, OLD_LIKELIHOOD
            FROM ItineraryAttraction
            ORDER BY ATTRACTION;
      """
   ).fetchall()

   assert accepted is True
   assert len( rows ) == len( attractions_to_keep )
   assert rows[ Position.FIRST ][ 'ATTRACTION' ] == kept_attraction
   assert rows[ Position.FIRST ][ 'OLD_LIKELIHOOD' ] is None


def Test_AcceptItinerary_TestZeroLikelihoodTransportations_ExpectAllRemoved(
      accept_itinerary_conn: sqlite3.Connection ) -> None:
   transportation = TransportationName.ZOOMOBILE
   _insert_transportation(
      accept_itinerary_conn,
      transportation=transportation,
      added_as_attraction=0,
      old_likelihood=100,
      new_likelihood=0 )
   _insert_transportation(
      accept_itinerary_conn,
      transportation=transportation,
      added_as_attraction=1,
      old_likelihood=80,
      new_likelihood=0 )

   accepted = AcceptItineraryProvider.accept_itinerary( accept_itinerary_conn )
   remaining_count = accept_itinerary_conn.execute(
      'SELECT COUNT(*) FROM ItineraryTransportation;'
   ).fetchone()[ Position.FIRST ]

   assert accepted is True
   assert remaining_count == 0
