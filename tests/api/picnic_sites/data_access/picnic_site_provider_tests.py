from __future__ import annotations

import sqlite3

import pytest

from api.picnic_sites.data_access.picnic_site_provider import PicnicSiteProvider

PICNIC_SITE_PROVIDER_SCHEMA = """
CREATE TABLE PicnicSite (
   X_COORD   REAL NOT NULL,
   Y_COORD   REAL NOT NULL,
   PRIMARY KEY ( X_COORD, Y_COORD )
);
"""

@pytest.fixture
def picnic_site_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( PICNIC_SITE_PROVIDER_SCHEMA )

   yield conn

   conn.close()

def Test_FetchPicnicSites_TestEmpty_ExpectEmptyList(
      picnic_site_provider_conn: sqlite3.Connection ) -> None:
   assert PicnicSiteProvider.fetch_picnic_sites( picnic_site_provider_conn ) == []

def Test_FetchPicnicSites_TestPopulated_ExpectMappedCoordinates(
      picnic_site_provider_conn: sqlite3.Connection ) -> None:
   picnic_site_provider_conn.execute(
      'INSERT INTO PicnicSite ( X_COORD, Y_COORD ) VALUES ( ?, ? );',
      ( 10.5, 20.25 ),
   )
   picnic_site_provider_conn.execute(
      'INSERT INTO PicnicSite ( X_COORD, Y_COORD ) VALUES ( ?, ? );',
      ( 3.0, 4.0 ),
   )
   picnic_site_provider_conn.commit()

   sites = PicnicSiteProvider.fetch_picnic_sites( picnic_site_provider_conn )

   assert { ( site.x_coord, site.y_coord ) for site in sites } == {
      ( 10.5, 20.25 ),
      ( 3.0, 4.0 ),
   }
