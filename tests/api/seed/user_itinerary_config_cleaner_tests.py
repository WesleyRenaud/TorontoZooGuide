from __future__ import annotations

import runpy
import sqlite3

import pytest

from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.seed.user_itinerary_config_cleaner import UserItineraryConfigCleaner
from api.shared.enums import ItineraryErrorType


STATUS_SCHEMA = """
CREATE TABLE ItineraryStatus (
   STATUS             TEXT NOT NULL PRIMARY KEY,
   IS_SUPPRESSABLE    BOOL NOT NULL
);

CREATE TABLE ItineraryStatusSuppression (
   STATUS             TEXT NOT NULL PRIMARY KEY,
   IS_SUPPRESSED      BOOL NOT NULL DEFAULT 0
);
"""


class _SharedConnection:
   def __init__( self, conn: sqlite3.Connection ) -> None:
      self._conn = conn
      self.calls: list[ str ] = []


   def cursor( self ) -> sqlite3.Cursor:
      self.calls.append( 'cursor' )
      return self._conn.cursor()


   def commit( self ) -> None:
      self.calls.append( 'commit' )
      self._conn.commit()


   def close( self ) -> None:
      self.calls.append( 'close' )


@pytest.fixture
def config_cleaner_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.executescript( STATUS_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryStatus (
               STATUS,
               IS_SUPPRESSABLE
            )
            VALUES ( ?, 1 );
      """,
      ( ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value, ) )
   conn.commit()

   yield conn

   conn.close()


def Test_Clear_TestSuppressedWarning_ExpectCleared(
      config_cleaner_conn: sqlite3.Connection ) -> None:
   ItineraryStatusProvider.suppress_itinerary_status(
      config_cleaner_conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   cur = config_cleaner_conn.cursor()
   UserItineraryConfigCleaner.clear( cur )
   config_cleaner_conn.commit()
   cur.close()

   assert not ItineraryStatusProvider.is_itinerary_error_suppressed(
      config_cleaner_conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def Test_Main_TestNoneSuppressed_ExpectReportsNoneEnabled(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ],
      config_cleaner_conn: sqlite3.Connection ) -> None:
   shared = _SharedConnection( config_cleaner_conn )
   monkeypatch.setattr(
      'api.seed.user_itinerary_config_cleaner.sqlite3.connect',
      lambda db_path: shared )

   UserItineraryConfigCleaner.main( db_path=':memory:' )

   assert shared.calls == [ 'cursor', 'cursor', 'commit', 'close' ]
   out = capsys.readouterr().out
   assert "No Don't show this again suppressions were enabled." in out
   assert 'User itinerary config cleared successfully.' in out


def Test_Main_TestSuppressedWarning_ExpectReportsClearedStatuses(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ],
      config_cleaner_conn: sqlite3.Connection ) -> None:
   ItineraryStatusProvider.suppress_itinerary_status(
      config_cleaner_conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   shared = _SharedConnection( config_cleaner_conn )
   monkeypatch.setattr(
      'api.seed.user_itinerary_config_cleaner.sqlite3.connect',
      lambda db_path: shared )

   UserItineraryConfigCleaner.main( db_path=':memory:' )

   out = capsys.readouterr().out
   assert (
      "Cleared Don't show this again for: "
      + ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value
      + '.' ) in out
   assert 'User itinerary config cleared successfully.' in out
   assert not ItineraryStatusProvider.is_itinerary_error_suppressed(
      config_cleaner_conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def Test_ModuleMain_TestMonkeypatchedConnect_ExpectClearCommitAndClose(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   real_connect = sqlite3.connect

   def connect_override( db_path: str ) -> sqlite3.Connection:
      if db_path == 'animals.db':
         conn = real_connect( ':memory:' )
         conn.executescript( STATUS_SCHEMA )
         return conn

      return real_connect( db_path )

   monkeypatch.setattr(
      'api.seed.user_itinerary_config_cleaner.sqlite3.connect',
      connect_override )

   runpy.run_module( 'api.seed.user_itinerary_config_cleaner', run_name='__main__' )

   out = capsys.readouterr().out
   assert "No Don't show this again suppressions were enabled." in out
   assert 'User itinerary config cleared successfully.' in out
