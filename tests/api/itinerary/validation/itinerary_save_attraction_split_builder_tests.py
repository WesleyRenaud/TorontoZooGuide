from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.validation.itinerary_save_attraction_split_builder import ItinerarySaveAttractionSplitBuilder


ATTRACTION_SCHEMA = """
CREATE TABLE Attraction (
   NAME                                 TEXT        NOT NULL PRIMARY KEY,
   IS_ALSO_TRANSPORTATION               INTEGER     NOT NULL DEFAULT 0
);
"""

CAROUSEL = 'Conservation Carousel'
ZOOMOBILE = 'Zoomobile'


@pytest.fixture
def split_builder_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ATTRACTION_SCHEMA )
   conn.execute(
      'INSERT INTO Attraction ( NAME, IS_ALSO_TRANSPORTATION ) VALUES ( ?, 0 );',
      ( CAROUSEL, ) )
   conn.execute(
      'INSERT INTO Attraction ( NAME, IS_ALSO_TRANSPORTATION ) VALUES ( ?, 1 );',
      ( ZOOMOBILE, ) )
   conn.commit()

   yield conn

   conn.close()


def Test_SplitNames_TestMixedAttractions_ExpectPlainAndTransportationLists(
      split_builder_conn: sqlite3.Connection ) -> None:
   plain_attractions, transportations = ItinerarySaveAttractionSplitBuilder.split_names(
      split_builder_conn,
      [ CAROUSEL, ZOOMOBILE, CAROUSEL ] )

   assert plain_attractions == [ CAROUSEL, CAROUSEL ]
   assert transportations == [ ZOOMOBILE ]


def Test_SplitNames_TestPlainAttractionsOnly_ExpectEmptyTransportations(
      split_builder_conn: sqlite3.Connection ) -> None:
   plain_attractions, transportations = ItinerarySaveAttractionSplitBuilder.split_names(
      split_builder_conn,
      [ CAROUSEL ] )

   assert plain_attractions == [ CAROUSEL ]
   assert transportations == []
