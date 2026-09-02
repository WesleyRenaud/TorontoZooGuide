from __future__ import annotations

import sqlite3

import pytest

from api.transportation.data_access.transportation_station_status_provider import TransportationStationStatusProvider
from api.transportation.status.transportation_station_closed_status import TransportationStationClosedStatus


TRANSPORTATION = 'Zoomobile'
STATION = 'Africa Zoomobile Station'
OTHER_STATION = 'Main Zoomobile Station'
CLOSED_MESSAGE = 'Station closed.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'

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
def transportation_station_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSPORTATION_STATION_STATUS_SCHEMA )

   yield conn

   conn.close()


def Test_FetchTransportationStationStatusRecords_TestEmpty_ExpectEmptyList(
      transportation_station_status_conn: sqlite3.Connection ) -> None:
   assert TransportationStationStatusProvider.fetch_transportation_station_status_records(
      transportation_station_status_conn,
      TRANSPORTATION ) == []


def Test_SaveClosedStatus_TestNewStation_ExpectPersistsAndFetches(
      transportation_station_status_conn: sqlite3.Connection ) -> None:
   assert TransportationStationStatusProvider.save_transportation_station_closed_status(
      transportation_station_status_conn,
      TRANSPORTATION,
      TransportationStationClosedStatus(
         transportation_station=STATION,
         start_date=START_DATE,
         end_date=END_DATE,
         message=CLOSED_MESSAGE ) ) is True

   records = TransportationStationStatusProvider.fetch_transportation_station_status_records(
      transportation_station_status_conn,
      TRANSPORTATION )

   assert len( records ) == 1
   assert records[ 0 ].station == STATION
   assert records[ 0 ].is_closed == 1
   assert records[ 0 ].closed_message == CLOSED_MESSAGE
   assert records[ 0 ].closed_start == START_DATE
   assert records[ 0 ].closed_end == END_DATE


def Test_SaveOpenStatus_TestClosedStation_ExpectDeletesRow(
      transportation_station_status_conn: sqlite3.Connection ) -> None:
   TransportationStationStatusProvider.save_transportation_station_closed_status(
      transportation_station_status_conn,
      TRANSPORTATION,
      TransportationStationClosedStatus(
         transportation_station=STATION,
         start_date=START_DATE,
         end_date=END_DATE,
         message=CLOSED_MESSAGE ) )
   TransportationStationStatusProvider.save_transportation_station_closed_status(
      transportation_station_status_conn,
      TRANSPORTATION,
      TransportationStationClosedStatus(
         transportation_station=OTHER_STATION,
         start_date=START_DATE,
         end_date=END_DATE,
         message=CLOSED_MESSAGE ) )

   assert TransportationStationStatusProvider.save_transportation_station_open_status(
      transportation_station_status_conn,
      TRANSPORTATION,
      STATION ) is True

   records = TransportationStationStatusProvider.fetch_transportation_station_status_records(
      transportation_station_status_conn,
      TRANSPORTATION )

   assert [ record.station for record in records ] == [ OTHER_STATION ]


def Test_SaveOpenStatus_TestMissingStation_ExpectFalse(
      transportation_station_status_conn: sqlite3.Connection ) -> None:
   assert TransportationStationStatusProvider.save_transportation_station_open_status(
      transportation_station_status_conn,
      TRANSPORTATION,
      STATION ) is False
