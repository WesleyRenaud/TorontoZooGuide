from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_exhibit_provider import ItineraryExhibitProvider


EXHIBIT_PROVIDER_SCHEMA = """
CREATE TABLE ItineraryExhibit (
   EXHIBIT              TEXT NOT NULL PRIMARY KEY
);
"""


@pytest.fixture
def exhibit_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( EXHIBIT_PROVIDER_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


def Test_SaveItineraryExhibits_TestSelectedExhibits_ExpectPersistedRows(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   cur = exhibit_provider_conn.cursor()
   ItineraryExhibitProvider.save_itinerary_exhibits(
      cur,
      [ 'Africa Savanna' ] )
   exhibit_provider_conn.commit()
   cur.close()

   saved_exhibits = exhibit_provider_conn.execute(
      """   SELECT EXHIBIT
            FROM ItineraryExhibit
            ORDER BY EXHIBIT;
      """ ).fetchall()

   assert [ row[ 'EXHIBIT' ] for row in saved_exhibits ] == [ 'Africa Savanna' ]


def Test_FetchItineraryExhibits_TestSavedExhibits_ExpectOrderedNames(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   cur = exhibit_provider_conn.cursor()
   ItineraryExhibitProvider.save_itinerary_exhibits(
      cur,
      [
         'Americas Outdoor Mayan Temple Ruins',
         'Africa Savanna',
      ] )
   exhibit_provider_conn.commit()
   cur.close()

   assert ItineraryExhibitProvider.fetch_itinerary_exhibits(
      exhibit_provider_conn ) == [
         'Americas Outdoor Mayan Temple Ruins',
         'Africa Savanna',
      ]


def Test_SaveItineraryExhibits_TestDuplicateExhibit_ExpectIgnored(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   cur = exhibit_provider_conn.cursor()
   ItineraryExhibitProvider.save_itinerary_exhibits(
      cur,
      [ 'Africa Savanna', 'Africa Savanna' ] )
   exhibit_provider_conn.commit()
   cur.close()

   assert ItineraryExhibitProvider.fetch_itinerary_exhibits(
      exhibit_provider_conn ) == [ 'Africa Savanna' ]
