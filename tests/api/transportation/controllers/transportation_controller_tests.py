from __future__ import annotations

from api_test_support.json_handler_test_double import JsonHandlerTestDouble
from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_transportation_coordinator import StubTransportationCoordinator
import pytest

from api import database_connection_provider as connection
import api.http_request_handler as server
from api.models.active_transportation_route import ActiveTransportationRoute
from api.models.transportation import Transportation
from api.models.transportation_station import TransportationStation
import api.request_connection_provider as request_connection
from api.transportation.controllers.transportation_controller import TransportationController
from api.transportation.coordinators.transportation_coordinator import TransportationCoordinator
from api.types import Types


TRANSPORTATION_NAME = 'Zoomobile'
STATION_NAME = 'Africa Zoomobile Station'
ROUTE_NAME = 'summer'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CLOSURE_MESSAGE = 'Closed.'


def _sample_transportation() -> Transportation:
   return Transportation(
      name=TRANSPORTATION_NAME,
      open_time='10:00 AM',
      close_time='4:00 PM' )


def _sample_route() -> ActiveTransportationRoute:
   return ActiveTransportationRoute(
      route=ROUTE_NAME,
      route_source='seasonal',
      transportation_stations=[
         TransportationStation(
            name=STATION_NAME,
            description='Station',
            x_coord=1.0,
            y_coord=2.0 )
      ] )


@pytest.fixture
def stub_transportation_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubTransportationCoordinator:
   StubTransportationCoordinator.instances = []
   StubTransportationCoordinator.default_success = True
   stub = StubTransportationCoordinator(
      transportations=[ _sample_transportation() ],
      transportation_routes=[ { 'name': ROUTE_NAME } ],
      transportation_route=_sample_route(),
      transportation_station_names=[ STATION_NAME ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubTransportationCoordinator.instances:
         StubTransportationCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, TransportationCoordinator, stub )

   return stub


def Test_GetTransportations_TestHttpRequest_ExpectMapsVisitDateAndReturnsTransportations(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   handler = make_handler(
      '/get-transportations',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'transportations' ] == [ _sample_transportation().to_dict() ]


def Test_GetTransportationRoutes_TestDirectCall_ExpectWritesRoutesFromCoordinator(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   TransportationController.get_transportation_routes( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'transportations': [ { 'name': ROUTE_NAME } ],
   }


def Test_GetTransportationRoute_TestHttpRequest_ExpectMapsRouteRequestAndReturnsRoute(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   handler = make_handler(
      '/get-transportation-route',
      {
         'transportationRoute': ROUTE_NAME,
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'transportationStationsToInclude': [ STATION_NAME ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result == _sample_route().to_dict()
   assert stub_transportation_coordinator.calls[ -1 ] == (
      'get_transportation_route',
      {
         'route': ROUTE_NAME,
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'transportation_stations_to_include': [ STATION_NAME ],
         'transportation': TRANSPORTATION_NAME,
      }
   )


def Test_GetTransportationStationNames_TestHttpRequest_ExpectDefaultsTransportationName(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   handler = make_handler( '/get-transportation-station-names', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'transportation_stations' ] == [ STATION_NAME ]
   assert stub_transportation_coordinator.calls[ -1 ] == (
      'get_transportation_station_names',
      { 'transportation': TRANSPORTATION_NAME },
   )


def Test_SetTransportationStationClosed_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   handler = make_handler(
      '/set-transportation-station-closed',
      {
         'transportationStation': STATION_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_transportation_coordinator.calls[ -1 ] == (
      'set_transportation_station_as_closed',
      {
         'transportation_station': STATION_NAME,
         'start_date': CLOSURE_START_DATE,
         'end_date': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
         'transportation': TRANSPORTATION_NAME,
      }
   )
   assert result[ 'success' ] is True


def Test_SetTransportationStationClosed_TestHttpRequest_ExpectCouldNotSetClosedApiError(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   StubTransportationCoordinator.default_success = False
   handler = make_handler(
      '/set-transportation-station-closed',
      { 'transportationStation': STATION_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotSetClosed'


def Test_SetTransportationStationOpen_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   handler = make_handler(
      '/set-transportation-station-open',
      { 'transportationStation': STATION_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_transportation_coordinator.calls[ -1 ] == (
      'set_transportation_station_as_open',
      {
         'transportation_station': STATION_NAME,
         'transportation': TRANSPORTATION_NAME,
      }
   )
   assert result[ 'success' ] is True


def Test_SetTransportationStationOpen_TestHttpRequest_ExpectCouldNotSetOpenApiError(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   StubTransportationCoordinator.default_success = False
   handler = make_handler(
      '/set-transportation-station-open',
      { 'transportationStation': STATION_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotSetOpen'


def Test_SetCurrentTransportationRoute_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   handler = make_handler(
      '/set-current-transportation-route',
      {
         'route': 'winter',
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_transportation_coordinator.calls[ -1 ] == (
      'set_current_transportation_route',
      {
         'route': 'winter',
         'start_date': CLOSURE_START_DATE,
         'end_date': CLOSURE_END_DATE,
         'transportation': TRANSPORTATION_NAME,
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'route' ] == 'winter'


def Test_SetCurrentTransportationRoute_TestHttpRequest_ExpectCouldNotSetTransportationRouteApiError(
      stub_transportation_coordinator: StubTransportationCoordinator ) -> None:
   StubTransportationCoordinator.default_success = False
   handler = make_handler(
      '/set-current-transportation-route',
      { 'route': 'winter' }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotSetTransportationRoute'
   assert result.get( 'apiErrorParams' ) == { 'route': 'winter' }
