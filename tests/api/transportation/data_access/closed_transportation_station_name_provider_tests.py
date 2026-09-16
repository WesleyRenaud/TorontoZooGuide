from __future__ import annotations

import sqlite3

import pytest

from api.shared.enums.transportation_name import TransportationName
from api.transportation.data_access.closed_transportation_station_name_provider import ClosedTransportationStationNameProvider


TODAY = '2026-09-16'
AFRICA = 'Africa Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'
MAIN = 'Main Zoomobile Station'
OTHER_TRANSPORTATION = 'Other'

TRANSPORTATION_STATION_STATUS_SCHEMA = """
CREATE TABLE TransportationStationStatus (
   TRANSPORTATION   TEXT NOT NULL,
   STATION          TEXT NOT NULL,
   IS_CLOSED        INTEGER NOT NULL,
   CLOSED_MESSAGE   TEXT,
   CLOSED_START     TEXT,
   CLOSED_END       TEXT,
   PRIMARY KEY ( TRANSPORTATION, STATION )
);
"""


@pytest.fixture
def closed_transportation_station_name_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSPORTATION_STATION_STATUS_SCHEMA )

   yield conn

   conn.close()


def _insert_status(
      conn: sqlite3.Connection,
      *,
      station: str,
      is_closed: int,
      start_date: str | None,
      end_date: str | None,
      transportation: str = TransportationName.ZOOMOBILE ) -> None:
   conn.execute(
      """   INSERT INTO TransportationStationStatus (
               TRANSPORTATION,
               STATION,
               IS_CLOSED,
               CLOSED_MESSAGE,
               CLOSED_START,
               CLOSED_END
            )
            VALUES ( ?, ?, ?, ?, ?, ? );
      """,
      (
         transportation,
         station,
         is_closed,
         'Station closed.',
         start_date,
         end_date,
      ) )
   conn.commit()


def Test_FetchClosedTransportationStationNames_TestEmpty_ExpectEmptyList(
      closed_transportation_station_name_conn: sqlite3.Connection ) -> None:
   assert ClosedTransportationStationNameProvider.fetch_closed_transportation_station_names(
      closed_transportation_station_name_conn,
      TransportationName.ZOOMOBILE,
      TODAY ) == []


def Test_FetchClosedTransportationStationNames_TestCurrentAndFuture_ExpectDistinctSortedStations(
      closed_transportation_station_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_transportation_station_name_conn,
      station=AFRICA,
      is_closed=1,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_status(
      closed_transportation_station_name_conn,
      station=EURASIA,
      is_closed=1,
      start_date='2026-10-01',
      end_date='2026-10-15' )

   assert ClosedTransportationStationNameProvider.fetch_closed_transportation_station_names(
      closed_transportation_station_name_conn,
      TransportationName.ZOOMOBILE,
      TODAY ) == [ AFRICA, EURASIA ]


def Test_FetchClosedTransportationStationNames_TestExpired_ExpectExcluded(
      closed_transportation_station_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_transportation_station_name_conn,
      station=AFRICA,
      is_closed=1,
      start_date='2026-08-01',
      end_date='2026-09-15' )

   assert ClosedTransportationStationNameProvider.fetch_closed_transportation_station_names(
      closed_transportation_station_name_conn,
      TransportationName.ZOOMOBILE,
      TODAY ) == []


def Test_FetchClosedTransportationStationNames_TestEndingToday_ExpectIncluded(
      closed_transportation_station_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_transportation_station_name_conn,
      station=AFRICA,
      is_closed=1,
      start_date='2026-09-01',
      end_date=TODAY )

   assert ClosedTransportationStationNameProvider.fetch_closed_transportation_station_names(
      closed_transportation_station_name_conn,
      TransportationName.ZOOMOBILE,
      TODAY ) == [ AFRICA ]


def Test_FetchClosedTransportationStationNames_TestOpenRow_ExpectExcluded(
      closed_transportation_station_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_transportation_station_name_conn,
      station=MAIN,
      is_closed=0,
      start_date='2026-09-01',
      end_date=None )

   assert ClosedTransportationStationNameProvider.fetch_closed_transportation_station_names(
      closed_transportation_station_name_conn,
      TransportationName.ZOOMOBILE,
      TODAY ) == []


def Test_FetchClosedTransportationStationNames_TestOtherTransportation_ExpectExcluded(
      closed_transportation_station_name_conn: sqlite3.Connection ) -> None:
   _insert_status(
      closed_transportation_station_name_conn,
      station=AFRICA,
      is_closed=1,
      start_date='2026-09-01',
      end_date='2026-09-30',
      transportation=OTHER_TRANSPORTATION )

   assert ClosedTransportationStationNameProvider.fetch_closed_transportation_station_names(
      closed_transportation_station_name_conn,
      TransportationName.ZOOMOBILE,
      TODAY ) == []
