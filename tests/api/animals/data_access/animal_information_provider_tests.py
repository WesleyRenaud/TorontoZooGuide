from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_information_provider import AnimalInformationProvider


SPECIES = 'Amur Tiger'
OTHER_SPECIES = 'Snow Leopard'
EXHIBIT = 'Eurasia Wilds'
OTHER_EXHIBIT = 'Canadian Domain'

ANIMAL_INFORMATION_PROVIDER_SCHEMA = """
CREATE TABLE Animal (
   SPECIES                     TEXT NOT NULL PRIMARY KEY,
   LATIN_NAME                  TEXT,
   MIN_TEMPERATURE             INTEGER,
   GENERAL_VIEWING_TIPS        TEXT,
   SEASONAL_VIEWING_TIPS       TEXT,
   IDENTIFICATION              TEXT,
   HABITAT_AND_RANGE           TEXT,
   DIET_AND_FEEDING            TEXT,
   BEHAVIOUR_AND_SOCIAL_LIFE   TEXT,
   ADAPTATIONS                 TEXT,
   REPRODUCTION_AND_LIFE_CYCLE TEXT,
   ANIMALS_AT_THE_ZOO          TEXT
);

CREATE TABLE Enclosure (
   SPECIES                       TEXT NOT NULL,
   EXHIBIT                       TEXT NOT NULL,
   SEASONAL_VIEWING_SUMMARY      TEXT NOT NULL,
   SEASONAL_VIEWING_INFORMATION  TEXT,
   INCLUDE_ALL_VIEWING_SPOTS     INTEGER,
   PRIMARY KEY ( SPECIES, EXHIBIT )
);
"""


@pytest.fixture
def animal_information_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_INFORMATION_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _insert_animal(
      conn: sqlite3.Connection,
      *,
      species: str = SPECIES ) -> None:
   conn.execute(
      """   INSERT INTO Animal (
               SPECIES,
               LATIN_NAME,
               GENERAL_VIEWING_TIPS,
               SEASONAL_VIEWING_TIPS,
               IDENTIFICATION,
               HABITAT_AND_RANGE,
               DIET_AND_FEEDING,
               BEHAVIOUR_AND_SOCIAL_LIFE,
               ADAPTATIONS,
               REPRODUCTION_AND_LIFE_CYCLE,
               ANIMALS_AT_THE_ZOO
            ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         species,
         'Panthera tigris altaica',
         'Look for striped coats.',
         'More active in cool weather.',
         'Large orange cat with stripes.',
         'Russian Far East.',
         'Meat.',
         'Solitary.',
         'Thick coat.',
         'Cubs stay with mother.',
         'Two adults on exhibit.',
      ),
   )


def _insert_enclosure(
      conn: sqlite3.Connection,
      *,
      species: str = SPECIES,
      exhibit: str = EXHIBIT ) -> None:
   conn.execute(
      """   INSERT INTO Enclosure (
               SPECIES,
               EXHIBIT,
               SEASONAL_VIEWING_SUMMARY,
               SEASONAL_VIEWING_INFORMATION,
               INCLUDE_ALL_VIEWING_SPOTS
            ) VALUES ( ?, ?, ?, ?, ? );
      """,
      (
         species,
         exhibit,
         'Best in morning.',
         'Outdoor yards preferred.',
         1,
      ),
   )


def Test_FetchAnimalInformation_TestMissing_ExpectNone(
      animal_information_provider_conn: sqlite3.Connection ) -> None:
   assert AnimalInformationProvider.fetch_animal_information(
      animal_information_provider_conn,
      SPECIES,
      EXHIBIT ) is None


def Test_FetchAnimalInformation_TestWrongExhibit_ExpectNone(
      animal_information_provider_conn: sqlite3.Connection ) -> None:
   _insert_animal( animal_information_provider_conn )
   _insert_enclosure( animal_information_provider_conn )
   animal_information_provider_conn.commit()

   assert AnimalInformationProvider.fetch_animal_information(
      animal_information_provider_conn,
      SPECIES,
      OTHER_EXHIBIT ) is None


def Test_FetchAnimalInformation_TestMatching_ExpectMappedAnimal(
      animal_information_provider_conn: sqlite3.Connection ) -> None:
   _insert_animal( animal_information_provider_conn )
   _insert_enclosure( animal_information_provider_conn )
   _insert_animal( animal_information_provider_conn, species=OTHER_SPECIES )
   _insert_enclosure(
      animal_information_provider_conn,
      species=OTHER_SPECIES,
      exhibit=OTHER_EXHIBIT )
   animal_information_provider_conn.commit()

   animal = AnimalInformationProvider.fetch_animal_information(
      animal_information_provider_conn,
      SPECIES,
      EXHIBIT )

   assert animal is not None
   assert animal.species == SPECIES
   assert animal.latin_name == 'Panthera tigris altaica'
   assert animal.general_viewing_tips == 'Look for striped coats.'
   assert animal.seasonal_viewing_tips == 'More active in cool weather.'
   assert animal.identification == 'Large orange cat with stripes.'
   assert animal.habitat_and_range == 'Russian Far East.'
   assert animal.diet_and_feeding == 'Meat.'
   assert animal.behaviour_and_life_cycle == 'Solitary.'
   assert animal.adaptations == 'Thick coat.'
   assert animal.reproduction_and_life_cycle == 'Cubs stay with mother.'
   assert animal.animals_at_the_zoo == 'Two adults on exhibit.'
   assert animal.exhibit == EXHIBIT
   assert animal.seasonal_viewing_summary == 'Best in morning.'
   assert animal.seasonal_viewing_information == 'Outdoor yards preferred.'
