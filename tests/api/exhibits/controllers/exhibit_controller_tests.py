from __future__ import annotations

from api_test_support.json_handler_test_double import JsonHandlerTestDouble
from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_exhibit_coordinator import StubExhibitCoordinator
import pytest

from api import database_connection_provider as connection
from api.exhibits.controllers.exhibit_controller import ExhibitController
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
import api.http_request_handler as server
import api.request_connection_provider as request_connection
from api.types import Types


REGION_NAME = 'Africa'
EXHIBIT_NAME = 'Africa Savanna'
OTHER_EXHIBIT_NAME = 'Eurasia Wilds'
ANIMAL_NAME = 'African Lion'
OTHER_ANIMAL_NAME = 'Amur Tiger'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CLOSURE_MESSAGE = 'Closed.'


@pytest.fixture
def stub_exhibit_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubExhibitCoordinator:
   StubExhibitCoordinator.instances = []
   StubExhibitCoordinator.default_success = True
   stub = StubExhibitCoordinator(
      region_name=REGION_NAME,
      exhibit_name=EXHIBIT_NAME,
      animal_names=[ ANIMAL_NAME, OTHER_ANIMAL_NAME ],
      exhibit_names=[ EXHIBIT_NAME, OTHER_EXHIBIT_NAME ],
      closed_exhibit_names=[ EXHIBIT_NAME ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubExhibitCoordinator.instances:
         StubExhibitCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, ExhibitCoordinator, stub )

   return stub


def Test_GetExhibitsInRegion_TestHttpRequest_ExpectMapsRegionAndReturnsExhibits(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   handler = make_handler(
      '/get-exhibits-in-region',
      { 'region': REGION_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'exhibits' ] == [ EXHIBIT_NAME ]
   assert stub_exhibit_coordinator.calls == [
      ( 'get_exhibits_in_region', { 'region': REGION_NAME } )
   ]


def Test_GetRegions_TestDirectCall_ExpectWritesRegionsFromCoordinator(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   ExhibitController.get_regions( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'regions': [
         {
            'name': REGION_NAME,
            'hasExhibits': True,
         }
      ],
   }
   assert stub_exhibit_coordinator.calls == [ ( 'get_regions', {} ) ]


def Test_GetAnimalNamesByExhibit_TestHttpRequest_ExpectMapsExhibitAndReturnsAnimals(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   handler = make_handler(
      '/get-animal-names-by-exhibit',
      { 'exhibit': EXHIBIT_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'animals' ] == [ ANIMAL_NAME, OTHER_ANIMAL_NAME ]
   assert stub_exhibit_coordinator.calls == [
      ( 'get_names_of_animals_in_exhibit', { 'exhibit': EXHIBIT_NAME } )
   ]


def Test_GetClosedExhibits_TestHttpRequest_ExpectMapsVisitDateAndReturnsClosedExhibits(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   handler = make_handler(
      '/get-closed-exhibits',
      {
         'month': VISIT_MONTH,
         'day': VISIT_DAY,
         'year': VISIT_YEAR,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'closed_exhibits' ] == [ EXHIBIT_NAME ]
   assert stub_exhibit_coordinator.calls == [
      (
         'get_closed_exhibits_for_visit_date',
         {
            'month': VISIT_MONTH,
            'day': VISIT_DAY,
            'year': VISIT_YEAR,
         }
      )
   ]


def Test_GetExhibitsByRegion_TestHttpRequest_ExpectRegionsResponseKey(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   handler = make_handler( '/get-exhibits-by-region', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'regions' ] == [
      {
         'name': REGION_NAME,
         'exhibits': [ EXHIBIT_NAME ],
      }
   ]
   assert stub_exhibit_coordinator.calls == [ ( 'get_regions_with_exhibits', {} ) ]


def Test_GetExhibits_TestDirectCall_ExpectWritesExhibitsFromCoordinator(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   ExhibitController.get_exhibits( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'exhibits': [ EXHIBIT_NAME, OTHER_EXHIBIT_NAME ],
   }
   assert stub_exhibit_coordinator.calls == [ ( 'get_exhibits', {} ) ]


def Test_SetExhibitClosed_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   handler = make_handler(
      '/set-exhibit-closed',
      {
         'exhibit': EXHIBIT_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_exhibit_coordinator.calls == [
      (
         'set_exhibit_as_closed',
         {
            'exhibit': EXHIBIT_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': CLOSURE_END_DATE,
            'message': CLOSURE_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'exhibit' ] == EXHIBIT_NAME
   assert result[ 'startDate' ] == CLOSURE_START_DATE
   assert result[ 'endDate' ] == CLOSURE_END_DATE
   assert result[ 'message' ] == CLOSURE_MESSAGE
   assert result.get( 'error' ) is None


def Test_SetExhibitClosed_TestHttpRequest_ExpectCouldNotSetClosedApiError(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   StubExhibitCoordinator.default_success = False
   handler = make_handler(
      '/set-exhibit-closed',
      { 'exhibit': EXHIBIT_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotSetClosed'
   assert result.get( 'apiErrorParams' ) == { 'name': EXHIBIT_NAME }


def Test_SetExhibitOpen_TestHttpRequest_ExpectCouldNotSetOpenApiError(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   StubExhibitCoordinator.default_success = False
   handler = make_handler(
      '/set-exhibit-open',
      { 'exhibit': EXHIBIT_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotSetOpen'
   assert result.get( 'apiErrorParams' ) == { 'name': EXHIBIT_NAME }


def Test_SetExhibitOpen_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_exhibit_coordinator: StubExhibitCoordinator ) -> None:
   handler = make_handler(
      '/set-exhibit-open',
      {
         'exhibit': EXHIBIT_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': None,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_exhibit_coordinator.calls == [
      (
         'set_exhibit_as_open',
         {
            'exhibit': EXHIBIT_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': None,
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'exhibit' ] == EXHIBIT_NAME
   assert result[ 'startDate' ] == CLOSURE_START_DATE
   assert result[ 'endDate' ] is None
   assert result.get( 'error' ) is None
