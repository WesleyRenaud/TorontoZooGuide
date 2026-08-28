from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_drinking_fountain_coordinator import StubDrinkingFountainCoordinator
import pytest

from api import database_connection_provider as connection
from api.drinking_fountains.controllers.drinking_fountain_controller import DrinkingFountainController
from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
import api.http_request_handler as server
from api.models.drinking_fountain import DrinkingFountain
import api.request_connection_provider as request_connection
from api.types import Types


VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CLOSURE_MESSAGE = 'Closed.'


def _sample_drinking_fountain() -> DrinkingFountain:
   return DrinkingFountain(
      x_coord=1.0,
      y_coord=2.0,
      is_closed=False,
      likelihood=1.0 )


@pytest.fixture
def stub_drinking_fountain_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubDrinkingFountainCoordinator:
   StubDrinkingFountainCoordinator.instances = []
   StubDrinkingFountainCoordinator.default_success = True
   stub = StubDrinkingFountainCoordinator(
      drinking_fountains=[ _sample_drinking_fountain() ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubDrinkingFountainCoordinator.instances:
         StubDrinkingFountainCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, DrinkingFountainCoordinator, stub )

   return stub


def Test_GetDrinkingFountains_TestHttpRequest_ExpectMapsVisitDateAndReturnsFountains(
      stub_drinking_fountain_coordinator: StubDrinkingFountainCoordinator ) -> None:
   handler = make_handler(
      '/get-drinking-fountains',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'drinking_fountains' ] == [ _sample_drinking_fountain().to_dict() ]


def Test_SetDrinkingFountainsClosed_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_drinking_fountain_coordinator: StubDrinkingFountainCoordinator ) -> None:
   handler = make_handler(
      '/set-drinking-fountains-closed',
      {
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_drinking_fountain_coordinator.calls == [
      (
         'set_drinking_fountains_as_closed',
         {
            'start_date': CLOSURE_START_DATE,
            'end_date': CLOSURE_END_DATE,
            'message': CLOSURE_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True


def Test_SetDrinkingFountainsClosed_TestHttpRequest_ExpectCouldNotSetClosedApiError(
      stub_drinking_fountain_coordinator: StubDrinkingFountainCoordinator ) -> None:
   StubDrinkingFountainCoordinator.default_success = False
   handler = make_handler( '/set-drinking-fountains-closed', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'drinkingFountainsCouldNotSetClosed'


def Test_SetDrinkingFountainsOpen_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_drinking_fountain_coordinator: StubDrinkingFountainCoordinator ) -> None:
   handler = make_handler(
      '/set-drinking-fountains-open',
      {
         'startDate': '2026-07-01',
         'endDate': None,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_drinking_fountain_coordinator.calls == [
      (
         'set_drinking_fountains_as_open',
         {
            'start_date': '2026-07-01',
            'end_date': None,
         }
      )
   ]
   assert result[ 'success' ] is True


def Test_SetDrinkingFountainsOpen_TestHttpRequest_ExpectCouldNotSetOpenApiError(
      stub_drinking_fountain_coordinator: StubDrinkingFountainCoordinator ) -> None:
   StubDrinkingFountainCoordinator.default_success = False
   handler = make_handler( '/set-drinking-fountains-open', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'drinkingFountainsCouldNotSetOpen'
