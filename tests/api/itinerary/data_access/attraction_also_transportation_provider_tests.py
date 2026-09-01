from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.attraction_also_transportation_provider import AttractionAlsoTransportationProvider


ATTRACTION_SCHEMA = """
CREATE TABLE Attraction (
   NAME                                 TEXT        NOT NULL PRIMARY KEY,
   IS_ALSO_TRANSPORTATION               INTEGER     NOT NULL DEFAULT 0
);
"""

CAROUSEL = 'Conservation Carousel'
ZOOMOBILE = 'Zoomobile'


@pytest.fixture
def attraction_conn() -> sqlite3.Connection:
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


def Test_AttractionIsAlsoTransportation_TestZoomobile_ExpectTrue(
      attraction_conn: sqlite3.Connection ) -> None:
   assert AttractionAlsoTransportationProvider.attraction_is_also_transportation(
      attraction_conn,
      ZOOMOBILE ) is True


def Test_AttractionIsAlsoTransportation_TestCarousel_ExpectFalse(
      attraction_conn: sqlite3.Connection ) -> None:
   assert AttractionAlsoTransportationProvider.attraction_is_also_transportation(
      attraction_conn,
      CAROUSEL ) is False


def Test_AttractionIsAlsoTransportation_TestMissingAttraction_ExpectFalse(
      attraction_conn: sqlite3.Connection ) -> None:
   assert AttractionAlsoTransportationProvider.attraction_is_also_transportation(
      attraction_conn,
      'Missing Attraction' ) is False


def Test_FetchAlsoTransportationAttractionNames_TestOwnedRows_ExpectZoomobileOnly(
      attraction_conn: sqlite3.Connection ) -> None:
   assert AttractionAlsoTransportationProvider.fetch_also_transportation_attraction_names(
      attraction_conn ) == { ZOOMOBILE }
