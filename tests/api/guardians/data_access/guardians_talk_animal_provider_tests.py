from __future__ import annotations

import sqlite3

import pytest

from api.guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider


PROVIDER_SCHEMA = """
CREATE TABLE GuardiansTalkAnimal (
   TALK_NAME        TEXT        NOT NULL,
   LOCATION         TEXT        NOT NULL,
   SPECIES          TEXT        NOT NULL,
   EXHIBIT          TEXT        NOT NULL,
   ENCLOSURE_NAME   TEXT
);
"""

PENGUIN_TALK = 'African Penguin'
GORILLA_TALK = 'Western Lowland Gorilla'
LION_TALK = 'African Lion'


@pytest.fixture
def guardians_talk_animal_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( PROVIDER_SCHEMA )
   conn.executemany(
      """   INSERT INTO GuardiansTalkAnimal (
               TALK_NAME,
               LOCATION,
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      [
         (
            PENGUIN_TALK,
            'Africa Savanna',
            'African Penguin',
            'Africa Savanna',
            'Outdoor',
         ),
         (
            GORILLA_TALK,
            'African Rainforest Pavilion',
            'Western Lowland Gorilla',
            'African Rainforest Pavilion',
            'Indoor',
         ),
         (
            LION_TALK,
            'Africa Savanna',
            'African Lion',
            'Africa Savanna',
            None,
         ),
      ],
   )
   conn.commit()

   yield conn

   conn.close()


def Test_FetchLinkedAnimals_TestPenguinTalk_ExpectSpeciesExhibitKey(
      guardians_talk_animal_provider_conn: sqlite3.Connection ) -> None:
   keys = GuardiansTalkAnimalProvider.fetch_linked_animals(
      guardians_talk_animal_provider_conn,
      PENGUIN_TALK )

   assert len( keys ) == 1
   assert keys[ 0 ].species == 'african penguin'
   assert keys[ 0 ].exhibit == 'africa savanna'


def Test_FetchAnimalLinks_TestPenguinTalk_ExpectOutdoorEnclosure(
      guardians_talk_animal_provider_conn: sqlite3.Connection ) -> None:
   links = GuardiansTalkAnimalProvider.fetch_animal_links(
      guardians_talk_animal_provider_conn,
      PENGUIN_TALK )

   assert len( links ) == 1
   assert links[ 0 ].species == 'African Penguin'
   assert links[ 0 ].enclosure_name == 'Outdoor'


def Test_FetchAnimalLinks_TestGorillaTalk_ExpectIndoorEnclosure(
      guardians_talk_animal_provider_conn: sqlite3.Connection ) -> None:
   links = GuardiansTalkAnimalProvider.fetch_animal_links(
      guardians_talk_animal_provider_conn,
      GORILLA_TALK )

   assert len( links ) == 1
   assert links[ 0 ].species == 'Western Lowland Gorilla'
   assert links[ 0 ].enclosure_name == 'Indoor'


def Test_FetchAnimalLinks_TestLionTalk_ExpectNullEnclosure(
      guardians_talk_animal_provider_conn: sqlite3.Connection ) -> None:
   links = GuardiansTalkAnimalProvider.fetch_animal_links(
      guardians_talk_animal_provider_conn,
      LION_TALK )

   assert len( links ) == 1
   assert links[ 0 ].species == 'African Lion'
   assert links[ 0 ].enclosure_name is None
