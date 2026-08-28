from __future__ import annotations

from api_test_support.json_handler_test_double import JsonHandlerTestDouble
from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_restroom_coordinator import StubRestroomCoordinator
import pytest

from api import database_connection_provider as connection
import api.http_request_handler as server
from api.models.restroom import Restroom
import api.request_connection_provider as request_connection
from api.restrooms.controllers.restroom_controller import RestroomController
from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from api.types import Types


RESTROOM_NAME = 'Entrance Restroom'
OTHER_RESTROOM_NAME = 'Africa Restroom'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CLOSURE_MESSAGE = 'Closed.'
ALERT_START_DATE = '2026-06-01'
ALERT_END_DATE = '2026-06-30'
ALERT_MESSAGE = "Women's restroom is temporarily unavailable."


def _sample_restroom() -> Restroom:
   return Restroom(
      title=RESTROOM_NAME,
      is_closed=False,
      has_alert=False )


@pytest.fixture
def stub_restroom_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubRestroomCoordinator:
   StubRestroomCoordinator.instances = []
   StubRestroomCoordinator.default_success = True
   stub = StubRestroomCoordinator(
      restroom_names=[ RESTROOM_NAME, OTHER_RESTROOM_NAME ],
      restrooms=[ _sample_restroom() ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubRestroomCoordinator.instances:
         StubRestroomCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, RestroomCoordinator, stub )

   return stub


def Test_GetRestrooms_TestHttpRequest_ExpectMapsVisitDateAndIncludeClosedToggle(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   handler = make_handler(
      '/get-restrooms',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'includeClosedRestrooms': True,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'restrooms' ] == [ _sample_restroom().to_dict() ]
   assert stub_restroom_coordinator.calls == [
      (
         'get_restrooms',
         {
            'day': VISIT_DAY,
            'month': VISIT_MONTH,
            'year': VISIT_YEAR,
            'include_closed_restrooms': True,
         }
      )
   ]


def Test_GetRestroomNames_TestDirectCall_ExpectWritesRestroomNamesFromCoordinator(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   RestroomController.get_restroom_names( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'restrooms': [ RESTROOM_NAME, OTHER_RESTROOM_NAME ],
   }


def Test_SetRestroomClosed_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   handler = make_handler(
      '/set-restroom-closed',
      {
         'restroom': RESTROOM_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_restroom_coordinator.calls == [
      (
         'set_restroom_as_closed',
         {
            'restroom': RESTROOM_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': CLOSURE_END_DATE,
            'message': CLOSURE_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True


def Test_SetRestroomClosed_TestHttpRequest_ExpectCouldNotSetClosedApiError(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   StubRestroomCoordinator.default_success = False
   handler = make_handler( '/set-restroom-closed', { 'restroom': RESTROOM_NAME } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotSetClosed'


def Test_SetRestroomOpen_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   handler = make_handler(
      '/set-restroom-open',
      {
         'restroom': RESTROOM_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': None,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_restroom_coordinator.calls == [
      (
         'set_restroom_as_open',
         {
            'restroom': RESTROOM_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': None,
         }
      )
   ]
   assert result[ 'success' ] is True


def Test_SetRestroomOpen_TestHttpRequest_ExpectCouldNotSetOpenApiError(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   StubRestroomCoordinator.default_success = False
   handler = make_handler( '/set-restroom-open', { 'restroom': RESTROOM_NAME } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotSetOpen'


def Test_SetRestroomAlert_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   handler = make_handler(
      '/set-restroom-alert',
      {
         'restroom': RESTROOM_NAME,
         'alertStartDate': ALERT_START_DATE,
         'alertEndDate': ALERT_END_DATE,
         'message': ALERT_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_restroom_coordinator.calls == [
      (
         'set_restroom_alert',
         {
            'restroom': RESTROOM_NAME,
            'alert_start_date': ALERT_START_DATE,
            'alert_end_date': ALERT_END_DATE,
            'message': ALERT_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'alertStartDate' ] == ALERT_START_DATE


def Test_SetRestroomAlert_TestHttpRequest_ExpectCouldNotSetRestroomAlertApiError(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   StubRestroomCoordinator.default_success = False
   handler = make_handler( '/set-restroom-alert', { 'restroom': RESTROOM_NAME } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotSetRestroomAlert'


def Test_RemoveRestroomAlert_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   handler = make_handler( '/remove-restroom-alert', { 'restroom': RESTROOM_NAME } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_restroom_coordinator.calls == [
      ( 'remove_restroom_alert', { 'restroom': RESTROOM_NAME } )
   ]
   assert result[ 'success' ] is True


def Test_RemoveRestroomAlert_TestHttpRequest_ExpectCouldNotRemoveRestroomAlertApiError(
      stub_restroom_coordinator: StubRestroomCoordinator ) -> None:
   StubRestroomCoordinator.default_success = False
   handler = make_handler( '/remove-restroom-alert', { 'restroom': RESTROOM_NAME } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotRemoveRestroomAlert'
