from __future__ import annotations

from api.transportation.status.transportation_station_status_builder import TransportationStationStatusBuilder


STATION_NAME = 'Africa Zoomobile Station'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
CUSTOM_MESSAGE = 'Station closed for route maintenance.'


def Test_BuildTransportationStationClosedStatus_TestCustomMessage_ExpectMappedStatus() -> None:
   status = TransportationStationStatusBuilder.build_transportation_station_closed_status(
      transportation_station=STATION_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CUSTOM_MESSAGE )

   assert status.transportation_station == STATION_NAME
   assert status.start_date == START_DATE
   assert status.end_date == END_DATE
   assert status.message == CUSTOM_MESSAGE


def Test_BuildTransportationStationClosedStatus_TestMissingMessage_ExpectDefaultClosedMessage() -> None:
   status = TransportationStationStatusBuilder.build_transportation_station_closed_status(
      transportation_station=STATION_NAME,
      start_date=START_DATE,
      end_date=None,
      message='' )

   assert status.end_date is None
   assert STATION_NAME in status.message
