from __future__ import annotations

from api_test_support.json_handler_test_double import JsonHandlerTestDouble
from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_animal_coordinator import StubAnimalCoordinator
import pytest

from api import database_connection_provider as connection
from api.animals.controllers.animal_controller import AnimalController
from api.animals.coordinators.animal_coordinator import AnimalCoordinator
import api.http_request_handler as server
import api.request_connection_provider as request_connection
from api.shared.constants import Constants
from api.shared.enums import AnimalViewingScope
from api.types import Types


ANIMAL_NAME = 'African Lion'
ANIMAL_EXHIBIT = 'Africa Savanna'
OTHER_ANIMAL_NAME = 'Amur Tiger'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
VISIT_TEMP = 22
OFF_DISPLAY_START_DATE = '2026-06-01'
OFF_DISPLAY_END_DATE = '2026-06-30'
OFF_DISPLAY_MESSAGE = 'Unavailable.'
VISIBILITY_SCHEDULE_START_DATE = '2026-06-01'
VISIBILITY_SCHEDULE_END_DATE = '2026-06-30'
VISIBILITY_SCHEDULE_DAILY_START_TIME = '09:00'
VISIBILITY_SCHEDULE_DAILY_END_TIME = '10:00'
VISIBILITY_SCHEDULE_MESSAGE = 'Morning only.'
VIEWING_ALERT_START_DATE = '2026-06-01'
VIEWING_ALERT_END_DATE = '2026-06-30'
VIEWING_ALERT_MESSAGE = 'Hard to spot.'


@pytest.fixture
def stub_animal_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubAnimalCoordinator:
   StubAnimalCoordinator.instances = []
   StubAnimalCoordinator.default_success = True
   stub = StubAnimalCoordinator(
      animal_name=ANIMAL_NAME,
      animal_exhibit=ANIMAL_EXHIBIT,
      species_names=[ ANIMAL_NAME, OTHER_ANIMAL_NAME ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubAnimalCoordinator.instances:
         StubAnimalCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, AnimalCoordinator, stub )

   return stub


def Test_GetAnimalsByExhibit_TestHttpRequest_ExpectMapsCoordinatorPayloadAndAnimalType(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-animals-by-exhibit',
      {
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'day': VISIT_DAY,
         'temp': VISIT_TEMP,
         'exhibitsToInclude': [ ANIMAL_EXHIBIT ]
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert stub_animal_coordinator.calls[ 0 ] == (
      'get_animals_viewable_on_day',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'temp': VISIT_TEMP,
         'include_off_display_animals': False,
         'for_itinerary': False,
         'threshold': None,
         'exhibits_to_include': [ ANIMAL_EXHIBIT ]
      }
   )


def Test_GetVisibleAnimals_TestHttpRequest_ExpectItineraryThresholdInCoordinatorCall(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-visible-animals',
      {
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'day': VISIT_DAY,
         'temp': VISIT_TEMP,
         'forItinerary': True
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert stub_animal_coordinator.calls[ 0 ] == (
      'get_animals_viewable_on_day',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'temp': VISIT_TEMP,
         'include_off_display_animals': False,
         'for_itinerary': True,
         'threshold': Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD,
      }
   )


def Test_GetVisibleAnimals_TestHttpRequest_ExpectMapsCoordinatorPayloadAndSpeciesResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-visible-animals',
      {
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'day': VISIT_DAY,
         'temp': VISIT_TEMP,
         'includeOffDisplayAnimals': True
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler )[ 'animals' ][ 0 ][ 'species' ] == ANIMAL_NAME
   assert stub_animal_coordinator.calls[ 0 ] == (
      'get_animals_viewable_on_day',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'temp': VISIT_TEMP,
         'include_off_display_animals': True,
         'for_itinerary': False,
         'threshold': None,
      }
   )


def Test_GetVisibleAnimals_TestHttpRequest_ExpectClosesDatabaseConnection(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-visible-animals',
      {
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'day': VISIT_DAY,
         'temp': VISIT_TEMP,
         'includeOffDisplayAnimals': True
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert stub_animal_coordinator.closed is True


def Test_GetAnimalViewingScopes_TestHttpRequest_ExpectViewingScopesResponseKey(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-animal-viewing-scopes',
      { 'species': ANIMAL_NAME, 'exhibit': ANIMAL_EXHIBIT }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert 'viewingScopes' in response_json( handler )


def Test_GetAnimalInformation_TestHttpRequest_ExpectInformationResponseKey(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-animal-information',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert 'information' in response_json( handler )


def Test_GetAnimalSpeciesNames_TestDirectCall_ExpectWritesSpeciesFromCoordinator(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   AnimalController.get_animal_species_names( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'species': [ ANIMAL_NAME, OTHER_ANIMAL_NAME ],
   }
   assert stub_animal_coordinator.calls == [ ( 'get_animal_species_names', {} ) ]


def Test_SetAnimalOffDisplay_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/set-animal-off-display',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT,
         'viewingScope': 'indoor',
         'startDate': OFF_DISPLAY_START_DATE,
         'endDate': OFF_DISPLAY_END_DATE,
         'message': OFF_DISPLAY_MESSAGE
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_animal_coordinator.calls == [
      (
         'set_animal_as_off_display',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
            'viewing_scope': AnimalViewingScope.INDOOR,
            'start_date': OFF_DISPLAY_START_DATE,
            'end_date': OFF_DISPLAY_END_DATE,
            'message': OFF_DISPLAY_MESSAGE
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'species' ] == ANIMAL_NAME
   assert result[ 'exhibit' ] == ANIMAL_EXHIBIT
   assert result[ 'viewingScope' ] == 'indoor'
   assert result[ 'startDate' ] == OFF_DISPLAY_START_DATE
   assert result[ 'endDate' ] == OFF_DISPLAY_END_DATE
   assert result[ 'message' ] == OFF_DISPLAY_MESSAGE
   assert result.get( 'error' ) is None


def Test_SetAnimalOffDisplay_TestHttpRequest_ExpectNoAnimalFoundApiError(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   StubAnimalCoordinator.default_success = False
   handler = make_handler(
      '/set-animal-off-display',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT,
         'viewingScope': 'all'
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'noAnimalFoundWithSpecies'
   assert result.get( 'apiErrorParams' ) == { 'species': ANIMAL_NAME }


def Test_SetAnimalOnDisplay_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/set-animal-on-display',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT,
         'viewingScope': 'outdoor'
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_animal_coordinator.calls == [
      (
         'set_animal_as_on_display',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
            'viewing_scope': AnimalViewingScope.OUTDOOR
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'species' ] == ANIMAL_NAME
   assert result[ 'exhibit' ] == ANIMAL_EXHIBIT
   assert result[ 'viewingScope' ] == 'outdoor'
   assert result.get( 'error' ) is None


def Test_SetAnimalVisibilitySchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/set-animal-visibility-schedule',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT,
         'scheduleStartDate': VISIBILITY_SCHEDULE_START_DATE,
         'scheduleEndDate': VISIBILITY_SCHEDULE_END_DATE,
         'dailyStartTime': VISIBILITY_SCHEDULE_DAILY_START_TIME,
         'dailyEndTime': VISIBILITY_SCHEDULE_DAILY_END_TIME,
         'message': VISIBILITY_SCHEDULE_MESSAGE
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_animal_coordinator.calls == [
      (
         'set_animal_limited_viewing_schedule',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
            'start_date': VISIBILITY_SCHEDULE_START_DATE,
            'end_date': VISIBILITY_SCHEDULE_END_DATE,
            'daily_start_time': VISIBILITY_SCHEDULE_DAILY_START_TIME,
            'daily_end_time': VISIBILITY_SCHEDULE_DAILY_END_TIME,
            'message': VISIBILITY_SCHEDULE_MESSAGE
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'species' ] == ANIMAL_NAME
   assert result[ 'exhibit' ] == ANIMAL_EXHIBIT
   assert result[ 'scheduleStartDate' ] == VISIBILITY_SCHEDULE_START_DATE
   assert result[ 'scheduleEndDate' ] == VISIBILITY_SCHEDULE_END_DATE
   assert result[ 'dailyStartTime' ] == VISIBILITY_SCHEDULE_DAILY_START_TIME
   assert result[ 'dailyEndTime' ] == VISIBILITY_SCHEDULE_DAILY_END_TIME
   assert result[ 'message' ] == VISIBILITY_SCHEDULE_MESSAGE
   assert result.get( 'error' ) is None


def Test_RemoveAnimalVisibilitySchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/remove-animal-visibility-schedule',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT,
         'viewingScope': 'all'
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_animal_coordinator.calls == [
      (
         'remove_animal_visibility_schedule',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'species' ] == ANIMAL_NAME
   assert result[ 'exhibit' ] == ANIMAL_EXHIBIT
   assert result.get( 'error' ) is None


def Test_SetAnimalViewingAlert_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/set-animal-viewing-alert',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT,
         'alertStartDate': VIEWING_ALERT_START_DATE,
         'alertEndDate': VIEWING_ALERT_END_DATE,
         'message': VIEWING_ALERT_MESSAGE
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_animal_coordinator.calls == [
      (
         'set_animal_viewing_alert',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
            'alert_start_date': VIEWING_ALERT_START_DATE,
            'alert_end_date': VIEWING_ALERT_END_DATE,
            'message': VIEWING_ALERT_MESSAGE
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'species' ] == ANIMAL_NAME
   assert result[ 'exhibit' ] == ANIMAL_EXHIBIT
   assert result[ 'alertStartDate' ] == VIEWING_ALERT_START_DATE
   assert result[ 'alertEndDate' ] == VIEWING_ALERT_END_DATE
   assert result[ 'message' ] == VIEWING_ALERT_MESSAGE
   assert result.get( 'error' ) is None


def Test_RemoveAnimalViewingAlert_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/remove-animal-viewing-alert',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_animal_coordinator.calls == [
      (
         'remove_animal_viewing_alert',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'species' ] == ANIMAL_NAME
   assert result[ 'exhibit' ] == ANIMAL_EXHIBIT
   assert result.get( 'error' ) is None


@pytest.mark.parametrize(
   'route, coordinator_method, api_error_type',
   [
      (
         '/set-animal-on-display',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
            'viewingScope': 'outdoor',
         },
         'noOffDisplayEntryFound',
      ),
      (
         '/set-animal-visibility-schedule',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
            'scheduleStartDate': VISIBILITY_SCHEDULE_START_DATE,
            'scheduleEndDate': VISIBILITY_SCHEDULE_END_DATE,
            'dailyStartTime': VISIBILITY_SCHEDULE_DAILY_START_TIME,
            'dailyEndTime': VISIBILITY_SCHEDULE_DAILY_END_TIME,
            'message': VISIBILITY_SCHEDULE_MESSAGE,
         },
         'couldNotSetLimitedViewingSchedule',
      ),
      (
         '/remove-animal-visibility-schedule',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
         },
         'couldNotRemoveVisibilitySchedule',
      ),
      (
         '/set-animal-viewing-alert',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
            'alertStartDate': VIEWING_ALERT_START_DATE,
            'alertEndDate': VIEWING_ALERT_END_DATE,
            'message': VIEWING_ALERT_MESSAGE,
         },
         'couldNotSetViewingAlert',
      ),
      (
         '/remove-animal-viewing-alert',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
         },
         'couldNotRemoveViewingAlert',
      ),
   ],
)
def Test_AnimalMutationEndpoints_TestCoordinatorFailure_ExpectApiError(
      stub_animal_coordinator: StubAnimalCoordinator,
      route: str,
      coordinator_method: dict[ str, str ],
      api_error_type: str ) -> None:
   StubAnimalCoordinator.default_success = False
   handler = make_handler( route, coordinator_method )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == api_error_type
