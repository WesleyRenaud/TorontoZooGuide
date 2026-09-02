from __future__ import annotations

import sqlite3

import pytest

from api.transportation.data_access.transportation_station_provider import TransportationStationProvider


TRANSPORTATION_STATION_PROVIDER_SCHEMA = """
CREATE TABLE TransportationStation (
   TRANSPORTATION     TEXT    NOT NULL,
   NAME               TEXT    NOT NULL,
   DESCRIPTION        TEXT    NOT NULL,
   X_COORD            REAL    NOT NULL,
   Y_COORD            REAL    NOT NULL,
   IS_MAIN_STATION    INTEGER NOT NULL DEFAULT 0,
   PRIMARY KEY ( TRANSPORTATION, NAME )
);
"""

ZOOMOBILE = 'Zoomobile'
TRAIN = 'Zoo Train'
MAIN = 'Main Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'


@pytest.fixture
def transportation_station_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSPORTATION_STATION_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _insert_station(
      conn: sqlite3.Connection,
      *,
      transportation: str,
      name: str,
      description: str,
      x_coord: float,
      y_coord: float,
      is_main_station: int = 0 ) -> None:
   conn.execute(
      """   INSERT INTO TransportationStation (
               TRANSPORTATION,
               NAME,
               DESCRIPTION,
               X_COORD,
               Y_COORD,
               IS_MAIN_STATION
            )
            VALUES ( ?, ?, ?, ?, ?, ? );
      """,
      (
         transportation,
         name,
         description,
         x_coord,
         y_coord,
         is_main_station,
      ),
   )


def _seed_zoomobile_stations( conn: sqlite3.Connection ) -> None:
   _insert_station(
      conn,
      transportation=ZOOMOBILE,
      name=MAIN,
      description='Main boarding area',
      x_coord=1.0,
      y_coord=2.0,
      is_main_station=1 )
   _insert_station(
      conn,
      transportation=ZOOMOBILE,
      name=AFRICA,
      description='Africa stop',
      x_coord=3.0,
      y_coord=4.0 )
   _insert_station(
      conn,
      transportation=TRAIN,
      name='Train Platform',
      description='Train only',
      x_coord=5.0,
      y_coord=6.0,
      is_main_station=1 )
   conn.commit()


def Test_FetchTransportationStationNames_TestEmpty_ExpectEmptyList(
      transportation_station_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationStationProvider.fetch_transportation_station_names(
      transportation_station_provider_conn,
      ZOOMOBILE ) == []


def Test_FetchTransportationStationNames_TestPopulated_ExpectFilteredNames(
      transportation_station_provider_conn: sqlite3.Connection ) -> None:
   _seed_zoomobile_stations( transportation_station_provider_conn )

   names = TransportationStationProvider.fetch_transportation_station_names(
      transportation_station_provider_conn,
      ZOOMOBILE )

   assert set( names ) == { MAIN, AFRICA }


def Test_FetchTransportationStationRecords_TestPopulated_ExpectMappedFields(
      transportation_station_provider_conn: sqlite3.Connection ) -> None:
   _seed_zoomobile_stations( transportation_station_provider_conn )

   records = TransportationStationProvider.fetch_transportation_station_records(
      transportation_station_provider_conn,
      ZOOMOBILE )

   by_name = { record.name: record for record in records }
   assert set( by_name ) == { MAIN, AFRICA }
   assert by_name[ MAIN ].description == 'Main boarding area'
   assert by_name[ MAIN ].x_coord == 1.0
   assert by_name[ MAIN ].y_coord == 2.0
   assert by_name[ AFRICA ].description == 'Africa stop'
   assert by_name[ AFRICA ].x_coord == 3.0
   assert by_name[ AFRICA ].y_coord == 4.0


def Test_FetchMainTransportationStationRecord_TestMissing_ExpectNone(
      transportation_station_provider_conn: sqlite3.Connection ) -> None:
   _insert_station(
      transportation_station_provider_conn,
      transportation=ZOOMOBILE,
      name=AFRICA,
      description='Africa stop',
      x_coord=3.0,
      y_coord=4.0 )
   transportation_station_provider_conn.commit()

   assert TransportationStationProvider.fetch_main_transportation_station_record(
      transportation_station_provider_conn,
      ZOOMOBILE ) is None


def Test_FetchMainTransportationStationRecord_TestPresent_ExpectMainStation(
      transportation_station_provider_conn: sqlite3.Connection ) -> None:
   _seed_zoomobile_stations( transportation_station_provider_conn )

   record = TransportationStationProvider.fetch_main_transportation_station_record(
      transportation_station_provider_conn,
      ZOOMOBILE )

   assert record is not None
   assert record.name == MAIN
   assert record.description == 'Main boarding area'
   assert record.x_coord == 1.0
   assert record.y_coord == 2.0


def Test_FetchTransportationStationRecord_TestMissing_ExpectNone(
      transportation_station_provider_conn: sqlite3.Connection ) -> None:
   _seed_zoomobile_stations( transportation_station_provider_conn )

   assert TransportationStationProvider.fetch_transportation_station_record(
      transportation_station_provider_conn,
      ZOOMOBILE,
      CANADA ) is None


def Test_FetchTransportationStationRecord_TestPresent_ExpectMappedFields(
      transportation_station_provider_conn: sqlite3.Connection ) -> None:
   _seed_zoomobile_stations( transportation_station_provider_conn )

   record = TransportationStationProvider.fetch_transportation_station_record(
      transportation_station_provider_conn,
      ZOOMOBILE,
      AFRICA )

   assert record is not None
   assert record.name == AFRICA
   assert record.description == 'Africa stop'
   assert record.x_coord == 3.0
   assert record.y_coord == 4.0
