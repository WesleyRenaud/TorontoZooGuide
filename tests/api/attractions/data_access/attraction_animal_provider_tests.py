from __future__ import annotations

import sqlite3

import pytest

from api.attractions.data_access.attraction_animal_provider import AttractionAnimalProvider


ATTRACTION_ANIMAL_SCHEMA = """
CREATE TABLE AttractionAnimal (
   ATTRACTION       VARCHAR(64) NOT NULL,
   SPECIES          VARCHAR(64) NOT NULL,
   EXHIBIT          VARCHAR(64) NOT NULL,
   ENCLOSURE_NAME   VARCHAR(64),
   PRIMARY KEY (ATTRACTION, SPECIES, EXHIBIT)
);
"""

KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'


@pytest.fixture
def attraction_animal_db() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ATTRACTION_ANIMAL_SCHEMA )
   conn.execute(
      """   INSERT INTO AttractionAnimal (
               ATTRACTION,
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, ?, ? );
      """,
      (
         KANGAROO_WALK_THRU,
         'Western Grey Kangaroo',
         'Australasia Outdoor',
         None,
      ) )
   conn.commit()
   yield conn
   conn.close()


def Test_FetchAttractionAnimalLinks_TestKangarooWalkThru_ExpectLinkedAnimal(
      attraction_animal_db: sqlite3.Connection ) -> None:
   links = AttractionAnimalProvider.fetch_attraction_animal_links(
      attraction_animal_db,
      KANGAROO_WALK_THRU )

   assert [
      (
         link.attraction,
         link.species,
         link.exhibit,
         link.enclosure_name,
      )
      for link in links
   ] == [
      (
         KANGAROO_WALK_THRU,
         'Western Grey Kangaroo',
         'Australasia Outdoor',
         None,
      ),
   ]


def Test_FetchAttractionLinkedAnimals_TestKangarooWalkThru_ExpectSpeciesExhibitKeys(
      attraction_animal_db: sqlite3.Connection ) -> None:
   keys = AttractionAnimalProvider.fetch_attraction_linked_animals(
      attraction_animal_db,
      KANGAROO_WALK_THRU )

   assert len( keys ) == 1
   assert keys[ 0 ].species == 'western grey kangaroo'
   assert keys[ 0 ].exhibit == 'australasia outdoor'
