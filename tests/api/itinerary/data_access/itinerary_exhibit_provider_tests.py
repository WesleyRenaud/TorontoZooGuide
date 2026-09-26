from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_exhibit_provider import ItineraryExhibitProvider
from api.itinerary.data_access.itinerary_save_input_mapper import ItinerarySaveInputMapper


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
   exhibit = 'Africa Savanna'
   selected_exhibits = [ exhibit ]
   cur = exhibit_provider_conn.cursor()

   ItineraryExhibitProvider.save_itinerary_exhibits(
      cur,
      selected_exhibits )
   exhibit_provider_conn.commit()
   cur.close()
   saved_exhibits = exhibit_provider_conn.execute(
      """   SELECT EXHIBIT
            FROM ItineraryExhibit
            ORDER BY EXHIBIT;
      """ ).fetchall()

   assert [ row[ 'EXHIBIT' ] for row in saved_exhibits ] == selected_exhibits


def Test_FetchItineraryExhibits_TestSavedExhibits_ExpectOrderedNames(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   selected_exhibits = [
      'Americas Outdoor Mayan Temple Ruins',
      'Africa Savanna',
   ]
   cur = exhibit_provider_conn.cursor()
   ItineraryExhibitProvider.save_itinerary_exhibits(
      cur,
      selected_exhibits )
   exhibit_provider_conn.commit()
   cur.close()

   exhibits = ItineraryExhibitProvider.fetch_itinerary_exhibits(
      exhibit_provider_conn )

   assert exhibits == selected_exhibits


def Test_SaveItineraryExhibits_TestDuplicateExhibit_ExpectIgnored(
      exhibit_provider_conn: sqlite3.Connection ) -> None:
   exhibit = 'Africa Savanna'
   selected_exhibits = [ exhibit, exhibit ]
   cur = exhibit_provider_conn.cursor()

   ItineraryExhibitProvider.save_itinerary_exhibits(
      cur,
      selected_exhibits )
   exhibit_provider_conn.commit()
   cur.close()
   exhibits = ItineraryExhibitProvider.fetch_itinerary_exhibits(
      exhibit_provider_conn )

   assert exhibits == ItinerarySaveInputMapper.map_named_strings(
      [ exhibit ] )
