from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_day_seasonal_viewability_provider import AnimalDaySeasonalViewabilityProvider
from api.animals.data_access.animal_day_seasonal_viewability_record import AnimalDaySeasonalViewabilityRecord
from api.shared.enums.position import Position


SPECIES = 'African Lion'
EXHIBIT = 'Africa Savanna'
SCHEMA = """
CREATE TABLE AnimalDaySeasonalViewabilityMultiplier (
   SPECIES  TEXT NOT NULL,
   EXHIBIT  TEXT NOT NULL,
   MONTH    INTEGER NOT NULL,
   DAY      INTEGER NOT NULL,
   VALUE    FLOAT NOT NULL
);
"""


@pytest.fixture
def viewability_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SCHEMA )
   conn.execute(
      """   INSERT INTO AnimalDaySeasonalViewabilityMultiplier (
               SPECIES,
               EXHIBIT,
               MONTH,
               DAY,
               VALUE
            ) VALUES ( ?, ?, ?, ?, ? )
      """,
      ( SPECIES, EXHIBIT, 11, 2, 0.5 ),
   )
   conn.commit()

   yield conn

   conn.close()


def Test_FetchRecords_TestSavedRow_ExpectMappedRecord(
      viewability_conn: sqlite3.Connection ) -> None:
   records = AnimalDaySeasonalViewabilityProvider.fetch_records( viewability_conn )

   assert records == [
      AnimalDaySeasonalViewabilityRecord(
         species=SPECIES,
         exhibit=EXHIBIT,
         month=11,
         day=2,
         value=0.5,
      ),
   ]
   assert records[ Position.FIRST ].value == 0.5
