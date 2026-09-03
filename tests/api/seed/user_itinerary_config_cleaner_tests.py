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


def Test_Main_TestMonkeypatchedConnect_ExpectClearCommitAndClose(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   calls: list[ str ] = []
   conn = sqlite3.connect( ':memory:' )
   cursor = conn.cursor()

   class _Conn:
      def cursor( self ) -> sqlite3.Cursor:
         calls.append( 'cursor' )
         return cursor


      def commit( self ) -> None:
         calls.append( 'commit' )


      def close( self ) -> None:
         calls.append( 'close' )

   monkeypatch.setattr(
      'api.seed.user_itinerary_config_cleaner.sqlite3.connect',
      lambda db_path: _Conn() )
   monkeypatch.setattr(
      UserItineraryConfigCleaner,
      'clear',
      classmethod( lambda cls, cur: calls.append( 'clear' ) ) )

   UserItineraryConfigCleaner.main( db_path=':memory:' )

   assert calls == [ 'cursor', 'clear', 'commit', 'close' ]
   assert 'User itinerary config cleared successfully.' in capsys.readouterr().out
   conn.close()


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

   assert 'User itinerary config cleared successfully.' in capsys.readouterr().out
