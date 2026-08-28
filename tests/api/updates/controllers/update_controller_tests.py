from __future__ import annotations

from api_test_support.json_handler_test_double import JsonHandlerTestDouble
from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_update_coordinator import StubUpdateCoordinator
import pytest

from api import database_connection_provider as connection
import api.http_request_handler as server
from api.models.update import Update
import api.request_connection_provider as request_connection
from api.types import Types
from api.updates.controllers.update_controller import UpdateController
from api.updates.coordinators.update_coordinator import UpdateCoordinator


UPDATE_TITLE = 'New baby giraffe'
UPDATE_DESCRIPTION = 'Come meet the new calf.'
UPDATE_TYPE = 'New Arrival'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026


def _sample_update() -> Update:
   return Update(
      title=UPDATE_TITLE,
      description=UPDATE_DESCRIPTION,
      update_type=UPDATE_TYPE,
      start_date=START_DATE,
      end_date=END_DATE )


@pytest.fixture
def stub_update_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubUpdateCoordinator:
   StubUpdateCoordinator.instances = []
   StubUpdateCoordinator.default_success = True
   stub = StubUpdateCoordinator(
      updates=[ _sample_update() ],
      active_updates=[ _sample_update() ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubUpdateCoordinator.instances:
         StubUpdateCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, UpdateCoordinator, stub )

   return stub


def Test_GetUpdates_TestHttpRequest_ExpectMapsVisitDateAndReturnsUpdates(
      stub_update_coordinator: StubUpdateCoordinator ) -> None:
   handler = make_handler(
      '/get-updates',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'updates' ] == [ _sample_update().to_dict() ]


def Test_GetActiveUpdateOptions_TestDirectCall_ExpectWritesUnexpiredUpdates(
      stub_update_coordinator: StubUpdateCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   UpdateController.get_active_update_options( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'updates': [ _sample_update().to_dict() ],
   }


def Test_CreateUpdate_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_update_coordinator: StubUpdateCoordinator ) -> None:
   handler = make_handler(
      '/create-update',
      {
         'title': UPDATE_TITLE,
         'description': UPDATE_DESCRIPTION,
         'type': UPDATE_TYPE,
         'startDate': START_DATE,
         'endDate': END_DATE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_update_coordinator.calls == [
      (
         'create_update',
         {
            'title': UPDATE_TITLE,
            'description': UPDATE_DESCRIPTION,
            'update_type': UPDATE_TYPE,
            'start_date': START_DATE,
            'end_date': END_DATE,
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'type' ] == UPDATE_TYPE


def Test_CreateUpdate_TestHttpRequest_ExpectOpenEndedDatesRetained(
      stub_update_coordinator: StubUpdateCoordinator ) -> None:
   handler = make_handler(
      '/create-update',
      {
         'title': 'Open-ended update',
         'description': UPDATE_DESCRIPTION,
         'type': 'Closure',
         'startDate': START_DATE,
         'endDate': None,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is True
   assert result[ 'endDate' ] is None


def Test_CreateUpdate_TestHttpRequest_ExpectCouldNotCreateUpdateApiError(
      stub_update_coordinator: StubUpdateCoordinator ) -> None:
   StubUpdateCoordinator.default_success = False
   handler = make_handler( '/create-update', { 'title': UPDATE_TITLE } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotCreateUpdate'


def Test_EndUpdate_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_update_coordinator: StubUpdateCoordinator ) -> None:
   handler = make_handler(
      '/end-update',
      {
         'title': UPDATE_TITLE,
         'startDate': START_DATE,
         'endDate': '2026-06-15',
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_update_coordinator.calls == [
      (
         'end_update',
         {
            'title': UPDATE_TITLE,
            'start_date': START_DATE,
            'end_date': '2026-06-15',
         }
      )
   ]
   assert result[ 'success' ] is True


def Test_EndUpdate_TestHttpRequest_ExpectCouldNotEndUpdateApiError(
      stub_update_coordinator: StubUpdateCoordinator ) -> None:
   StubUpdateCoordinator.default_success = False
   handler = make_handler( '/end-update', { 'title': UPDATE_TITLE } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotEndUpdate'


def Test_EditUpdate_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_update_coordinator: StubUpdateCoordinator ) -> None:
   handler = make_handler(
      '/edit-update',
      {
         'title': UPDATE_TITLE,
         'startDate': START_DATE,
         'description': 'Updated calf details.',
         'type': 'Closure',
         'endDate': '2026-07-15',
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_update_coordinator.calls == [
      (
         'edit_update',
         {
            'title': UPDATE_TITLE,
            'start_date': START_DATE,
            'description': 'Updated calf details.',
            'update_type': 'Closure',
            'end_date': '2026-07-15',
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'type' ] == 'Closure'


def Test_EditUpdate_TestHttpRequest_ExpectCouldNotEditUpdateApiError(
      stub_update_coordinator: StubUpdateCoordinator ) -> None:
   StubUpdateCoordinator.default_success = False
   handler = make_handler( '/edit-update', { 'title': UPDATE_TITLE } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotEditUpdate'
