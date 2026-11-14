from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.restroom_notice_checker import RestroomNoticeChecker
from tools.checks.restroom_notice_reader import RestroomNoticeReader
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 14 )
SCHEMA = """
CREATE TABLE Restroom (
   TITLE TEXT NOT NULL,
   X_COORD REAL NOT NULL,
   Y_COORD REAL NOT NULL,
   PRIMARY KEY (TITLE)
);

CREATE TABLE RestroomStatus (
   RESTROOM TEXT NOT NULL,
   IS_CLOSED INTEGER NOT NULL DEFAULT 0,
   CLOSED_MESSAGE TEXT,
   CLOSED_START TEXT,
   CLOSED_END TEXT,
   PRIMARY KEY (RESTROOM)
);

CREATE TABLE RestroomAlert (
   RESTROOM TEXT NOT NULL,
   ALERT_MESSAGE TEXT NOT NULL,
   ALERT_START_DATE TEXT,
   ALERT_END_DATE TEXT,
   PRIMARY KEY (RESTROOM)
);
"""


def page( boxes: list[ str ] ) -> str:
   body = ''.join( f'<div class="box">{ box }</div>' for box in boxes )
   return f'<h2 id="notices">Notices</h2>{ body }<h2 id="animals">Animals</h2>'


def database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO Restroom ( TITLE, X_COORD, Y_COORD ) VALUES ( ?, 0, 0 )',
      [
         ( 'African Rainforest Restroom', ),
         ( 'Eurasia Restroom', ),
         ( 'Entrance Restroom', ),
         ( 'Zootique Restroom', ),
      ],
   )
   connection.commit()
   connection.close()


def insert_status(
      path: Path,
      restroom: str,
      is_closed: int,
      message: str | None,
      start: str,
      end: str | None ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO RestroomStatus (
               RESTROOM, IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
            ) VALUES ( ?, ?, ?, ?, ? )
      """,
      ( restroom, is_closed, message, start, end ),
   )
   connection.commit()
   connection.close()


def insert_alert(
      path: Path,
      restroom: str,
      message: str,
      start: str,
      end: str ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO RestroomAlert (
               RESTROOM, ALERT_MESSAGE, ALERT_START_DATE, ALERT_END_DATE
            ) VALUES ( ?, ?, ?, ? )
      """,
      ( restroom, message, start, end ),
   )
   connection.commit()
   connection.close()


def status_rows( path: Path ) -> dict[ str, tuple[ int, str | None, str | None, str | None ] ]:
   connection = sqlite3.connect( path )
   loaded = {
      row[ 0 ]: ( row[ 1 ], row[ 2 ], row[ 3 ], row[ 4 ] )
      for row in connection.execute(
         """   SELECT RESTROOM, IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
               FROM RestroomStatus
         """
      )
   }
   connection.close()
   return loaded


def alert_rows( path: Path ) -> dict[ str, tuple[ str, str | None, str | None ] ]:
   connection = sqlite3.connect( path )
   loaded = {
      row[ 0 ]: ( row[ 1 ], row[ 2 ], row[ 3 ] )
      for row in connection.execute(
         """   SELECT RESTROOM, ALERT_MESSAGE, ALERT_START_DATE, ALERT_END_DATE
               FROM RestroomAlert
         """
      )
   }
   connection.close()
   return loaded


def Test_CheckSchedules_TestWebsiteNotices_ExpectClosureAndAlert(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         (
            '<p><strong>Africa Savanna Loop Detour</strong> '
            'The washrooms, pathway in front of the African Rainforest Pavilion, '
            'and Multi-Faith Prayer and Spiritual Space are closed due to construction.</p>'
         ),
         (
            '<p><strong>Zootique</strong> '
            'The washroom in the Zootique/Learning and Engagement Building '
            'will open late due to maintenance.</p>'
         ),
      ] ),
   )
   CheckReport.reset_fixed_count()

   result = RestroomNoticeChecker.check_schedules( database_path, TODAY )

   assert result == 0
   assert status_rows( database_path )[ 'African Rainforest Restroom' ][ 0 ] == 1
   assert status_rows( database_path )[ 'African Rainforest Restroom' ][ 2 : ] == (
      '2026-11-14',
      '2026-12-14',
   )
   assert alert_rows( database_path )[ 'Zootique Restroom' ][ 1 : ] == (
      '2026-11-14',
      '2026-12-14',
   )


def Test_CheckSchedules_TestStaleRows_ExpectCleared( tmp_path: Path, monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_status(
      database_path,
      'Eurasia Restroom',
      1,
      'The Eurasia washrooms are closed.',
      '2026-11-01',
      '2026-12-01',
   )
   insert_alert(
      database_path,
      'Entrance Restroom',
      'The women\'s washroom located at the front entrance will open late.',
      '2026-11-01',
      '2026-12-01',
   )
   insert_alert(
      database_path,
      'Zootique Restroom',
      'The washroom will open late.',
      '2026-06-01',
      '2026-06-01',
   )
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: page( [
         '<p><strong>Pavilion</strong> The indoor habitat is closed for maintenance.</p>',
      ] ),
   )
   CheckReport.reset_fixed_count()

   RestroomNoticeChecker.check_schedules( database_path, TODAY )

   assert status_rows( database_path )[ 'Eurasia Restroom' ][ 0 ] == 0
   assert 'Entrance Restroom' not in alert_rows( database_path )
   assert alert_rows( database_path )[ 'Zootique Restroom' ][ 1 : ] == (
      '2026-06-01',
      '2026-06-01',
   )


def Test_CheckSchedules_TestSameSentence_ExpectEndMovedForward(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   html = page( [
      (
         '<p><strong>Eurasia</strong> '
         'The Eurasia washrooms are closed for maintenance.</p>'
      ),
   ] )
   message = RestroomNoticeReader.read( html )[ 0 ].message
   insert_status( database_path, 'Eurasia Restroom', 1, message, '2026-11-01', '2026-11-20' )
   monkeypatch.setattr( WebsitePage, 'fetch_text', lambda url: html )
   CheckReport.reset_fixed_count()

   RestroomNoticeChecker.check_schedules( database_path, TODAY )

   assert status_rows( database_path )[ 'Eurasia Restroom' ] == (
      1,
      message,
      '2026-11-01',
      '2026-12-14',
   )
