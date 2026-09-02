from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import cast

import pytest

from api.models.active_transportation_route import ActiveTransportationRoute
from api.models.transportation import Transportation
from api.models.transportation_station import TransportationStation
from api.request_connection_provider import RequestConnectionProvider
from api.shared.enums.transportation_name import TransportationName
from api.shared.opening_schedule_visit_context import OpeningScheduleVisitContext
from api.shared.opening_schedule_visit_context_resolver import OpeningScheduleVisitContextResolver
from api.transportation.coordinators.transportation_coordinator import TransportationCoordinator
from api.transportation.data_access.transportation_active_route_provider import TransportationActiveRouteProvider
from api.transportation.data_access.transportation_provider import TransportationProvider
from api.transportation.data_access.transportation_record import TransportationRecord
from api.transportation.data_access.transportation_route_provider import TransportationRouteProvider
from api.transportation.data_access.transportation_route_schedule_provider import TransportationRouteScheduleProvider
from api.transportation.data_access.transportation_station_provider import TransportationStationProvider
from api.transportation.data_access.transportation_station_status_provider import TransportationStationStatusProvider
from api.transportation.domain.active_transportation_route_builder import ActiveTransportationRouteBuilder
from api.transportation.domain.transportation_builder import TransportationBuilder
from api.transportation.domain.transportation_route_builder import TransportationRouteBuilder
from api.transportation.domain.transportation_route_context import TransportationRouteContext
from api.transportation.domain.transportation_route_stations_builder import TransportationRouteStationsBuilder
from api.transportation.scheduling.transportation_current_route_schedule import TransportationCurrentRouteSchedule
from api.transportation.scheduling.transportation_current_route_schedule_builder import TransportationCurrentRouteScheduleBuilder
from api.transportation.search.transportation_stations_matching_query_builder import TransportationStationsMatchingQueryBuilder
from api.transportation.search.transportations_matching_query_builder import TransportationsMatchingQueryBuilder
from api.transportation.status.transportation_station_closed_status import TransportationStationClosedStatus
from api.transportation.status.transportation_station_status_builder import TransportationStationStatusBuilder
from api.types import Types


VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026
TARGET_DATE = date( 2026, 6, 15 )
ROUTE = 'summer'
QUERY = 'zoo'
STATION_NAME = 'Main Zoomobile Station'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Station closed for maintenance.'
TRANSPORTATION = TransportationName.ZOOMOBILE

TRANSPORTATION_MODEL = Transportation(
   name=TRANSPORTATION,
   open_time='10:00 AM',
   close_time='4:00 PM' )
STATION = TransportationStation(
   name=STATION_NAME,
   description='Station',
   x_coord=1.0,
   y_coord=2.0 )
VISIT_CONTEXT = OpeningScheduleVisitContext(
   normalized_month=6,
   normalized_day=15,
   target_date=TARGET_DATE,
   weekday=0,
   is_weekend_or_holiday=False )
ROUTE_CONTEXT = TransportationRouteContext(
   normalized_month=6,
   normalized_day=15,
   target_date=TARGET_DATE )


@dataclass
class StubConnection():
   pass


STUB_CONNECTION = cast( Types.Connection, StubConnection() )


@pytest.fixture
def stub_request_connection( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: STUB_CONNECTION )


def Test_GetTransportations_TestProviderAndBuilder_ExpectTransportations(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   records = [ object() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      OpeningScheduleVisitContextResolver,
      'resolve',
      lambda **_kwargs: VISIT_CONTEXT )
   monkeypatch.setattr(
      TransportationProvider,
      'fetch_transportation_records',
      lambda _conn, *, visit_date: records if visit_date == TARGET_DATE else [] )

   def build_transportations(
         fetched: list[ TransportationRecord ],
         *,
         context: OpeningScheduleVisitContext ) -> list[ Transportation ]:
      captured[ 'records' ] = fetched
      captured[ 'context' ] = context
      return [ TRANSPORTATION_MODEL ]

   monkeypatch.setattr(
      TransportationBuilder,
      'build_transportations',
      build_transportations )

   assert TransportationCoordinator.get_transportations(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR ) == [ TRANSPORTATION_MODEL ]
   assert captured[ 'records' ] is records
   assert captured[ 'context' ] is VISIT_CONTEXT


def Test_GetTransportationsMatchingQuery_TestBuilder_ExpectMatches(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   transportations = [ TRANSPORTATION_MODEL ]

   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportations',
      lambda **_kwargs: transportations )
   monkeypatch.setattr(
      TransportationsMatchingQueryBuilder,
      'build',
      lambda rows, query: rows if query == QUERY else [] )

   assert TransportationCoordinator.get_transportations_matching_query(
      query=QUERY,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR ) == transportations


def Test_GetTransportationRoutes_TestGroupedRoutes_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   route_rows = [ object() ]
   grouped = [ { 'name': ROUTE } ]

   monkeypatch.setattr(
      TransportationRouteProvider,
      'fetch_transportation_routes_by_name',
      lambda _conn: route_rows )
   monkeypatch.setattr(
      TransportationRouteBuilder,
      'group_transportation_routes',
      lambda rows: grouped if rows is route_rows else [] )

   assert TransportationCoordinator.get_transportation_routes() == grouped


def Test_GetTransportationStationNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationStationProvider,
      'fetch_transportation_station_names',
      lambda _conn, transportation: [ STATION_NAME ]
      if transportation == TRANSPORTATION
      else [] )

   assert TransportationCoordinator.get_transportation_station_names() == [ STATION_NAME ]


def Test_GetTransportationRouteIds_TestProviderIds_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_transportation_route_ids',
      lambda _conn, transportation: [ ROUTE ]
      if transportation == TRANSPORTATION
      else [] )

   assert TransportationCoordinator.get_transportation_route_ids() == [ ROUTE ]


def Test_GetTransportationStations_TestBuildersAndProviders_ExpectStations(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   station_records = [ object() ]
   status_records = [ object() ]
   stations_on_route = [ STATION_NAME ]
   station_context = object()
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      TransportationStationProvider,
      'fetch_transportation_station_records',
      lambda _conn, transportation: station_records )
   monkeypatch.setattr(
      TransportationStationStatusProvider,
      'fetch_transportation_station_status_records',
      lambda _conn, transportation: status_records )
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_transportation_route_station_names',
      lambda _conn, transportation, *, route: stations_on_route if route == ROUTE else [] )
   monkeypatch.setattr(
      TransportationRouteStationsBuilder,
      'resolve_transportation_station_context',
      lambda **kwargs: station_context )

   def build_route_stations( **kwargs: object ) -> list[ TransportationStation ]:
      captured.update( kwargs )
      return [ STATION ]

   monkeypatch.setattr(
      TransportationRouteStationsBuilder,
      'build_route_transportation_stations',
      build_route_stations )

   assert TransportationCoordinator.get_transportation_stations(
      route=ROUTE,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR ) == [ STATION ]
   assert captured[ 'station_records' ] is station_records
   assert captured[ 'status_records' ] is status_records
   assert captured[ 'context' ] is station_context


def Test_GetTransportationStationsMatchingQuery_TestResolvedRoute_ExpectMatches(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   stations = [ STATION ]
   matched = [ STATION ]

   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'resolve_transportation_route_context',
      lambda **_kwargs: ROUTE_CONTEXT )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_route_ids',
      lambda *_args, **_kwargs: [ ROUTE ] )
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_active_transportation_route',
      lambda *_args, **_kwargs: ROUTE )
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_transportation_day_route',
      lambda *_args, **_kwargs: ROUTE )
   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'resolve_requested_transportation_route',
      lambda *_args, **_kwargs: ( ROUTE, 'manual' ) )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_stations',
      lambda **kwargs: stations if kwargs[ 'route' ] == ROUTE else [] )
   monkeypatch.setattr(
      TransportationStationsMatchingQueryBuilder,
      'build',
      lambda rows, query: matched if rows is stations and query == QUERY else [] )

   assert TransportationCoordinator.get_transportation_stations_matching_query(
      query=QUERY,
      route=ROUTE,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR ) == matched


def Test_GetTransportationRoute_TestResolvedRoute_ExpectActiveRoute(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   stations = [ STATION ]
   expected = ActiveTransportationRoute(
      route=ROUTE,
      route_source='manual',
      transportation_stations=stations )

   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'resolve_transportation_route_context',
      lambda **_kwargs: ROUTE_CONTEXT )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_route_ids',
      lambda *_args, **_kwargs: [ ROUTE ] )
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_active_transportation_route',
      lambda *_args, **_kwargs: ROUTE )
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_transportation_day_route',
      lambda *_args, **_kwargs: ROUTE )
   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'resolve_requested_transportation_route',
      lambda *_args, **_kwargs: ( ROUTE, 'manual' ) )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_stations',
      lambda **_kwargs: stations )
   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'build_active_transportation_route_response',
      lambda **kwargs: expected
      if kwargs[ 'route' ] == ROUTE and kwargs[ 'route_source' ] == 'manual'
      else None )

   assert TransportationCoordinator.get_transportation_route(
      route=ROUTE,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR ) == expected


def Test_GetActiveTransportationRoute_TestValidRoute_ExpectRoute(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_active_transportation_route',
      lambda *_args, **_kwargs: ROUTE )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_route_ids',
      lambda *_args, **_kwargs: [ ROUTE ] )
   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'is_valid_transportation_route',
      lambda route, valid_routes: route in valid_routes )

   assert TransportationCoordinator.get_active_transportation_route(
      TARGET_DATE ) == ROUTE


def Test_GetActiveTransportationRoute_TestInvalidRoute_ExpectNone(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_active_transportation_route',
      lambda *_args, **_kwargs: 'winter' )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_route_ids',
      lambda *_args, **_kwargs: [ ROUTE ] )
   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'is_valid_transportation_route',
      lambda route, valid_routes: route in valid_routes )

   assert TransportationCoordinator.get_active_transportation_route(
      TARGET_DATE ) is None


def Test_GetTransportationDayRoute_TestValidRoute_ExpectRoute(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_transportation_day_route',
      lambda *_args, **_kwargs: ROUTE )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_route_ids',
      lambda *_args, **_kwargs: [ ROUTE ] )
   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'is_valid_transportation_route',
      lambda route, valid_routes: route in valid_routes )

   assert TransportationCoordinator.get_transportation_day_route(
      month=VISIT_MONTH,
      day=VISIT_DAY ) == ROUTE


def Test_GetTransportationDayRoute_TestInvalidRoute_ExpectNone(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationActiveRouteProvider,
      'fetch_transportation_day_route',
      lambda *_args, **_kwargs: None )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_route_ids',
      lambda *_args, **_kwargs: [ ROUTE ] )
   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'is_valid_transportation_route',
      lambda route, valid_routes: route in valid_routes )

   assert TransportationCoordinator.get_transportation_day_route(
      month=VISIT_MONTH,
      day=VISIT_DAY ) is None


def Test_SetTransportationStationAsClosed_TestBuiltStatus_ExpectSaved(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   status = TransportationStationClosedStatus(
      transportation_station=STATION_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE )
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      TransportationStationStatusBuilder,
      'build_transportation_station_closed_status',
      lambda **_kwargs: status )

   def save(
         _conn: Types.Connection,
         transportation: str,
         *,
         status: TransportationStationClosedStatus ) -> bool:
      captured[ 'transportation' ] = transportation
      captured[ 'status' ] = status
      return True

   monkeypatch.setattr(
      TransportationStationStatusProvider,
      'save_transportation_station_closed_status',
      save )

   assert TransportationCoordinator.set_transportation_station_as_closed(
      transportation_station=STATION_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE ) is True
   assert captured[ 'transportation' ] == TRANSPORTATION
   assert captured[ 'status' ] is status


def Test_SetTransportationStationAsOpen_TestProvider_ExpectSaved(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   def save(
         _conn: Types.Connection,
         transportation: str,
         *,
         transportation_station: str ) -> bool:
      captured[ 'transportation' ] = transportation
      captured[ 'station' ] = transportation_station
      return True

   monkeypatch.setattr(
      TransportationStationStatusProvider,
      'save_transportation_station_open_status',
      save )

   assert TransportationCoordinator.set_transportation_station_as_open(
      STATION_NAME ) is True
   assert captured == {
      'transportation': TRANSPORTATION,
      'station': STATION_NAME,
   }


def Test_SetCurrentTransportationRoute_TestInvalidRoute_ExpectFalse(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_route_ids',
      lambda *_args, **_kwargs: [ ROUTE ] )
   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'is_valid_transportation_route',
      lambda route, valid_routes: False )

   assert TransportationCoordinator.set_current_transportation_route(
      route='winter',
      start_date=START_DATE,
      end_date=END_DATE ) is False


def Test_SetCurrentTransportationRoute_TestValidRoute_ExpectSaved(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   schedule = TransportationCurrentRouteSchedule(
      route=ROUTE,
      start_date=START_DATE,
      end_date=END_DATE )
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_route_ids',
      lambda *_args, **_kwargs: [ ROUTE ] )
   monkeypatch.setattr(
      ActiveTransportationRouteBuilder,
      'is_valid_transportation_route',
      lambda route, valid_routes: route in valid_routes )
   monkeypatch.setattr(
      TransportationCurrentRouteScheduleBuilder,
      'build_current_transportation_route_schedule',
      lambda **_kwargs: schedule )

   def save(
         _conn: Types.Connection,
         transportation: str,
         *,
         schedule: TransportationCurrentRouteSchedule ) -> bool:
      captured[ 'transportation' ] = transportation
      captured[ 'schedule' ] = schedule
      return True

   monkeypatch.setattr(
      TransportationRouteScheduleProvider,
      'save_current_transportation_route_schedule',
      save )

   assert TransportationCoordinator.set_current_transportation_route(
      route=ROUTE,
      start_date=START_DATE,
      end_date=END_DATE ) is True
   assert captured[ 'transportation' ] == TRANSPORTATION
   assert captured[ 'schedule' ] is schedule
