from __future__ import annotations

from pathlib import Path
import runpy
import sqlite3

import pytest

from api.database_connection_provider import DatabaseConnectionProvider
from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.seed.user_itinerary_config_cleaner import UserItineraryConfigCleaner
from api.shared.enums import ItineraryErrorType


STATUS_SCHEMA = """
CREATE TABLE ItineraryStatus (
   STATUS             TEXT NOT NULL PRIMARY KEY,
   IS_SUPPRESSABLE    BOOL NOT NULL
);
"""


def _prepare_animals_db( path: Path ) -> None:
   conn = sqlite3.connect( path )
   conn.executescript( STATUS_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryStatus (
               STATUS,
               IS_SUPPRESSABLE
            )
            VALUES ( ?, 1 );
      """,
      ( ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value, ),
   )
   conn.commit()
   conn.close()
   DatabaseConnectionProvider.ensure_itinerary_schema( DatabaseConnectionProvider.itinerary_path_beside( path ) )


@pytest.fixture
def config_cleaner_db( tmp_path: Path ) -> Path:
   path = tmp_path / 'animals.db'
   _prepare_animals_db( path )

   return path


def Test_Clear_TestSuppressedWarning_ExpectCleared(
      config_cleaner_db: Path ) -> None:
   conn = DatabaseConnectionProvider.open( str( config_cleaner_db ) )
   ItineraryStatusProvider.suppress_itinerary_status(
      conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   cur = conn.cursor()
   UserItineraryConfigCleaner.clear( cur )
   conn.commit()
   cur.close()

   suppressed = ItineraryStatusProvider.is_itinerary_error_suppressed(
      conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
   DatabaseConnectionProvider.close( conn )

   assert not suppressed


def Test_Main_TestNoneSuppressed_ExpectReportsNoneEnabled(
      config_cleaner_db: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   UserItineraryConfigCleaner.main( db_path=str( config_cleaner_db ) )

   out = capsys.readouterr().out
   assert "No Don't show this again suppressions were enabled." in out
   assert 'User itinerary config cleared successfully.' in out


def Test_Main_TestSuppressedWarning_ExpectReportsClearedStatuses(
      config_cleaner_db: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   conn = DatabaseConnectionProvider.open( str( config_cleaner_db ) )
   ItineraryStatusProvider.suppress_itinerary_status(
      conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
   conn.commit()
   DatabaseConnectionProvider.close( conn )

   UserItineraryConfigCleaner.main( db_path=str( config_cleaner_db ) )

   conn = DatabaseConnectionProvider.open( str( config_cleaner_db ) )
   suppressed = ItineraryStatusProvider.is_itinerary_error_suppressed(
      conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
   DatabaseConnectionProvider.close( conn )
   out = capsys.readouterr().out

   assert (
      "Cleared Don't show this again for: "
      + ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value
      + '.' ) in out
   assert 'User itinerary config cleared successfully.' in out
   assert not suppressed


def Test_ModuleMain_TestDefaultAnimalsPath_ExpectClearSucceeds(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   path = tmp_path / 'animals.db'
   _prepare_animals_db( path )
   real_open = DatabaseConnectionProvider.open

   def open_override( db_path: str = 'animals.db' ) -> sqlite3.Connection:
      if db_path == 'animals.db':
         return real_open( str( path ) )

      return real_open( db_path )

   monkeypatch.setattr(
      DatabaseConnectionProvider,
      'open',
      classmethod( lambda cls, db_path='animals.db': open_override( db_path ) ) )

   runpy.run_module( 'api.seed.user_itinerary_config_cleaner', run_name='__main__' )

   out = capsys.readouterr().out
   assert "No Don't show this again suppressions were enabled." in out
   assert 'User itinerary config cleared successfully.' in out
