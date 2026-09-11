from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest

from api.seed.user_itinerary_date_backdater import UserItineraryDateBackdater
from api.shared.enums.position import Position


BACKDATER_SCHEMA = """
CREATE TABLE ItineraryDate (
   ITINERARY_DATE       TEXT,
   ARRIVAL_TIME         TEXT,
   DEPARTURE_TIME       TEXT
);
"""


@pytest.fixture
def backdater_conn( tmp_path: Path ) -> sqlite3.Connection:
   path = tmp_path / 'animals.db'
   conn = sqlite3.connect( path )
   conn.executescript( BACKDATER_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryDate ( ITINERARY_DATE, ARRIVAL_TIME, DEPARTURE_TIME )
            VALUES ( '2026-06-15', '09:30', '16:00' );
      """ )
   conn.commit()

   yield conn

   conn.close()


def Test_BackdateToYesterday_TestExistingDate_ExpectYesterday(
      backdater_conn: sqlite3.Connection ) -> None:
   cur = backdater_conn.cursor()
   yesterday = ( date.today() - timedelta( days=1 ) ).isoformat()

   result = UserItineraryDateBackdater.backdate_to_yesterday( cur )
   backdater_conn.commit()
   cur.close()

   stored = backdater_conn.execute(
      'SELECT ITINERARY_DATE FROM ItineraryDate;' ).fetchone()[ Position.FIRST ]

   assert result == yesterday
   assert stored == yesterday


def Test_BackdateToYesterday_TestEmptyTable_ExpectNone(
      tmp_path: Path ) -> None:
   path = tmp_path / 'empty.db'
   conn = sqlite3.connect( path )
   conn.executescript( BACKDATER_SCHEMA )
   conn.commit()
   cur = conn.cursor()

   result = UserItineraryDateBackdater.backdate_to_yesterday( cur )
   conn.commit()
   cur.close()
   conn.close()

   assert result is None


def Test_Main_TestDatabasePath_ExpectBackdatesAndPrints(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   path = tmp_path / 'animals.db'
   conn = sqlite3.connect( path )
   conn.executescript( BACKDATER_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryDate ( ITINERARY_DATE )
            VALUES ( '2026-06-15' );
      """ )
   conn.commit()
   conn.close()

   yesterday = ( date.today() - timedelta( days=1 ) ).isoformat()
   UserItineraryDateBackdater.main( str( path ) )

   conn = sqlite3.connect( path )
   stored = conn.execute(
      'SELECT ITINERARY_DATE FROM ItineraryDate;' ).fetchone()[ Position.FIRST ]
   conn.close()

   assert stored == yesterday
   assert f'Itinerary date backdated to { yesterday }.' in capsys.readouterr().out


def Test_Main_TestEmptyTable_ExpectPrintsNoRowMessage(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   path = tmp_path / 'animals.db'
   conn = sqlite3.connect( path )
   conn.executescript( BACKDATER_SCHEMA )
   conn.commit()
   conn.close()

   UserItineraryDateBackdater.main( str( path ) )

   assert 'No itinerary date row to backdate. Save an itinerary first.' in (
      capsys.readouterr().out )
