from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from tools.checks.check_report import CheckReport
from tools.checks.zoomobile_route import ZoomobileRoute
from tools.checks.zoomobile_route_checker import ZoomobileRouteChecker
from tools.checks.zoomobile_route_reader import ZoomobileRouteReader


TODAY = date( 2026, 11, 14 )
SCHEMA = """
CREATE TABLE TransportationRoute (
   TRANSPORTATION TEXT NOT NULL,
   ROUTE TEXT NOT NULL,
   PRIMARY KEY (TRANSPORTATION, ROUTE)
);

CREATE TABLE TransportationRouteSchedule (
   TRANSPORTATION TEXT NOT NULL,
   SCHEDULE_START_DATE TEXT NOT NULL,
   SCHEDULE_END_DATE TEXT,
   ROUTE TEXT NOT NULL,
   PRIMARY KEY (TRANSPORTATION, SCHEDULE_START_DATE)
);
"""


def database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      'INSERT INTO TransportationRoute ( TRANSPORTATION, ROUTE ) VALUES ( ?, ? )',
      [ ( 'Zoomobile', 'summer' ), ( 'Zoomobile', 'winter' ) ],
   )
   connection.commit()
   connection.close()


def insert_route( path: Path, route: str, start: str, end: str ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO TransportationRouteSchedule (
               TRANSPORTATION, SCHEDULE_START_DATE, SCHEDULE_END_DATE, ROUTE
            ) VALUES ( 'Zoomobile', ?, ?, ? )
      """,
      ( start, end, route ),
   )
   connection.commit()
   connection.close()


def rows( path: Path ) -> list[ tuple[ str, str, str | None ] ]:
   connection = sqlite3.connect( path )
   loaded = list( connection.execute(
      """   SELECT ROUTE, SCHEDULE_START_DATE, SCHEDULE_END_DATE
            FROM TransportationRouteSchedule
            ORDER BY SCHEDULE_START_DATE
      """
   ) )
   connection.close()
   return loaded


def Test_CheckSchedules_TestSummerInNovember_ExpectTwoWeeks(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   monkeypatch.setattr(
      ZoomobileRouteReader,
      'read',
      lambda: ZoomobileRoute( 'summer' ),
   )
   CheckReport.reset_fixed_count()

   result = ZoomobileRouteChecker.check_schedules( database_path, TODAY )
   output = capsys.readouterr().out

   assert result == 0
   assert rows( database_path ) == [ ( 'summer', '2026-11-14', '2026-11-28' ) ]
   assert 'Set the route to Summer until November 28, 2026.' in output


def Test_CheckSchedules_TestLongerSummer_ExpectTrimmed(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_route( database_path, 'summer', '2026-11-01', '2026-12-31' )
   monkeypatch.setattr(
      ZoomobileRouteReader,
      'read',
      lambda: ZoomobileRoute( 'summer' ),
   )
   CheckReport.reset_fixed_count()

   ZoomobileRouteChecker.check_schedules( database_path, TODAY )

   assert rows( database_path ) == [ ( 'summer', '2026-11-01', '2026-11-28' ) ]


def Test_CheckSchedules_TestWinterStored_ExpectSummerFromToday(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_route( database_path, 'winter', '2026-11-08', '2027-04-30' )
   monkeypatch.setattr(
      ZoomobileRouteReader,
      'read',
      lambda: ZoomobileRoute( 'summer' ),
   )
   CheckReport.reset_fixed_count()

   ZoomobileRouteChecker.check_schedules( database_path, TODAY )

   assert rows( database_path ) == [
      ( 'winter', '2026-11-08', '2026-11-13' ),
      ( 'summer', '2026-11-14', '2026-11-28' ),
   ]


def Test_CheckSchedules_TestAprilSummer_ExpectFullSummer(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_route( database_path, 'winter', '2026-11-01', '2027-04-30' )
   monkeypatch.setattr(
      ZoomobileRouteReader,
      'read',
      lambda: ZoomobileRoute( 'summer' ),
   )
   CheckReport.reset_fixed_count()

   ZoomobileRouteChecker.check_schedules( database_path, date( 2027, 4, 15 ) )

   assert rows( database_path ) == [
      ( 'winter', '2026-11-01', '2027-04-14' ),
      ( 'summer', '2027-04-15', '2027-10-31' ),
   ]
