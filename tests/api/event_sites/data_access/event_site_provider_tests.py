from __future__ import annotations

import sqlite3

import pytest

from api.event_sites.data_access.event_site_provider import EventSiteProvider


EVENT_SITE_PROVIDER_SCHEMA = """
CREATE TABLE EventSite (
   NAME      TEXT NOT NULL PRIMARY KEY,
   X_COORD   REAL NOT NULL,
   Y_COORD   REAL NOT NULL
);
"""

CELEBRATION_SITE = 'Celebration Site'


@pytest.fixture
def event_site_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( EVENT_SITE_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def Test_FetchEventSites_TestEmpty_ExpectEmptyList(
      event_site_provider_conn: sqlite3.Connection ) -> None:
   assert EventSiteProvider.fetch_event_sites( event_site_provider_conn ) == []


def Test_FetchEventSites_TestPopulated_ExpectMappedFields(
      event_site_provider_conn: sqlite3.Connection ) -> None:
   event_site_provider_conn.execute(
      """   INSERT INTO EventSite (
               NAME,
               X_COORD,
               Y_COORD
            )
            VALUES ( ?, ?, ? );
      """,
      ( CELEBRATION_SITE, 10.0, 20.0 ),
   )
   event_site_provider_conn.commit()

   sites = EventSiteProvider.fetch_event_sites( event_site_provider_conn )

   assert len( sites ) == 1
   assert sites[ 0 ].name == CELEBRATION_SITE
   assert sites[ 0 ].x_coord == 10.0
   assert sites[ 0 ].y_coord == 20.0
