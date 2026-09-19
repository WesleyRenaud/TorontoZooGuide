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
from api.animals.domain.animal_viewing_scope import AnimalViewingScope
import api.http_request_handler as server
import api.request_connection_provider as request_connection
from api.shared.constants import Constants
from api.shared.enums.api_error_type import ApiErrorType
from api.shared.enums.position import Position
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
         StubAnimalCoordinator.instances[ Position.LAST ].closed = True

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
   assert result[ 'animals' ][ Position.FIRST ][ 'type' ] == 'animal'
   assert stub_animal_coordinator.calls[ Position.FIRST ] == (
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
   assert stub_animal_coordinator.calls[ Position.FIRST ] == (
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
   assert response_json( handler )[ 'animals' ][ Position.FIRST ][ 'species' ] == ANIMAL_NAME
   assert stub_animal_coordinator.calls[ Position.FIRST ] == (
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


def Test_GetExhibitsForSpecies_TestHttpRequest_ExpectMapsSpeciesAndExhibitsResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-exhibits-for-species',
      { 'species': ANIMAL_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_exhibits_for_species',
         {
            'species': ANIMAL_NAME,
         }
      )
   ]


def Test_GetOffDisplayAnimalOptions_TestHttpRequest_ExpectMapsExhibitAndSpeciesResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-off-display-animal-options',
      { 'exhibit': ANIMAL_EXHIBIT }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'species': [ ANIMAL_NAME, OTHER_ANIMAL_NAME ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_off_display_animal_options',
         {
            'exhibit': ANIMAL_EXHIBIT,
         }
      )
   ]


def Test_GetOffDisplayAnimalOptions_TestDirectCallWithoutExhibit_ExpectCoordinatorGetsNone(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   AnimalController.get_off_display_animal_options( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'species': [ ANIMAL_NAME, OTHER_ANIMAL_NAME ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_off_display_animal_options',
         {
            'exhibit': None,
         }
      )
   ]


def Test_GetOffDisplayExhibitOptions_TestDirectCall_ExpectWritesExhibitsFromCoordinator(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   AnimalController.get_off_display_exhibit_options( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [ ( 'get_off_display_exhibit_options', { 'species': None } ) ]


def Test_GetOffDisplayExhibitOptions_TestHttpRequest_ExpectWritesExhibitsFromCoordinator(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler( '/get-off-display-exhibit-options', {} )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [ ( 'get_off_display_exhibit_options', { 'species': None } ) ]


def Test_GetOffDisplayExhibitOptions_TestHttpRequestWithSpecies_ExpectMapsSpecies(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-off-display-exhibit-options',
      { 'species': ANIMAL_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_off_display_exhibit_options',
         {
            'species': ANIMAL_NAME,
         }
      )
   ]


def Test_GetOffDisplayViewingScopeOptions_TestHttpRequest_ExpectViewingScopesResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-off-display-viewing-scope-options',
      { 'species': ANIMAL_NAME, 'exhibit': ANIMAL_EXHIBIT }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'viewingScopes': [
         { 'enclosureName': 'Indoor', 'label': 'Indoor' },
         { 'enclosureName': 'Outdoor', 'label': 'Outdoor' },
      ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_off_display_viewing_scope_options',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
         }
      )
   ]


def Test_GetAnimalVisibilityScheduleOptions_TestHttpRequest_ExpectMapsExhibitAndSpeciesResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-animal-visibility-schedule-options',
      { 'exhibit': ANIMAL_EXHIBIT }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'species': [ ANIMAL_NAME, OTHER_ANIMAL_NAME ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_animal_visibility_schedule_options',
         {
            'exhibit': ANIMAL_EXHIBIT,
         }
      )
   ]


def Test_GetAnimalVisibilityScheduleOptions_TestDirectCallWithoutExhibit_ExpectCoordinatorGetsNone(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   AnimalController.get_animal_visibility_schedule_options( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'species': [ ANIMAL_NAME, OTHER_ANIMAL_NAME ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_animal_visibility_schedule_options',
         {
            'exhibit': None,
         }
      )
   ]


def Test_GetAnimalVisibilityScheduleExhibitOptions_TestDirectCall_ExpectWritesExhibitsFromCoordinator(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   AnimalController.get_animal_visibility_schedule_exhibit_options( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [ ( 'get_animal_visibility_schedule_exhibit_options', { 'species': None } ) ]


def Test_GetAnimalVisibilityScheduleExhibitOptions_TestHttpRequest_ExpectWritesExhibitsFromCoordinator(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler( '/get-animal-visibility-schedule-exhibit-options', {} )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [ ( 'get_animal_visibility_schedule_exhibit_options', { 'species': None } ) ]


def Test_GetAnimalVisibilityScheduleExhibitOptions_TestHttpRequestWithSpecies_ExpectMapsSpecies(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-animal-visibility-schedule-exhibit-options',
      { 'species': ANIMAL_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_animal_visibility_schedule_exhibit_options',
         {
            'species': ANIMAL_NAME,
         }
      )
   ]


def Test_GetAnimalViewingAlertOptions_TestHttpRequest_ExpectMapsExhibitAndSpeciesResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-animal-viewing-alert-options',
      { 'exhibit': ANIMAL_EXHIBIT }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'species': [ ANIMAL_NAME, OTHER_ANIMAL_NAME ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_animal_viewing_alert_options',
         {
            'exhibit': ANIMAL_EXHIBIT,
         }
      )
   ]


def Test_GetAnimalViewingAlertOptions_TestDirectCallWithoutExhibit_ExpectCoordinatorGetsNone(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   AnimalController.get_animal_viewing_alert_options( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'species': [ ANIMAL_NAME, OTHER_ANIMAL_NAME ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_animal_viewing_alert_options',
         {
            'exhibit': None,
         }
      )
   ]


def Test_GetAnimalViewingAlertExhibitOptions_TestDirectCall_ExpectWritesExhibitsFromCoordinator(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   AnimalController.get_animal_viewing_alert_exhibit_options( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [ ( 'get_animal_viewing_alert_exhibit_options', { 'species': None } ) ]


def Test_GetAnimalViewingAlertExhibitOptions_TestHttpRequest_ExpectWritesExhibitsFromCoordinator(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler( '/get-animal-viewing-alert-exhibit-options', {} )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [ ( 'get_animal_viewing_alert_exhibit_options', { 'species': None } ) ]


def Test_GetAnimalViewingAlertExhibitOptions_TestHttpRequestWithSpecies_ExpectMapsSpecies(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/get-animal-viewing-alert-exhibit-options',
      { 'species': ANIMAL_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler ) == {
      'exhibits': [ ANIMAL_EXHIBIT ],
   }
   assert stub_animal_coordinator.calls == [
      (
         'get_animal_viewing_alert_exhibit_options',
         {
            'species': ANIMAL_NAME,
         }
      )
   ]


def Test_SetAnimalOffDisplay_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/set-animal-off-display',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT,
         'viewingScopes': [ 'Male Herd' ],
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
            'viewing_scopes': [
               AnimalViewingScope.from_enclosure_name( 'Male Herd' ),
            ],
            'start_date': OFF_DISPLAY_START_DATE,
            'end_date': OFF_DISPLAY_END_DATE,
            'message': OFF_DISPLAY_MESSAGE
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'species' ] == ANIMAL_NAME
   assert result[ 'exhibit' ] == ANIMAL_EXHIBIT
   assert result[ 'viewingScopes' ] == [
      {
         'enclosureName': 'Male Herd',
         'label': 'Male Herd',
      },
   ]
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
         'viewingScopes': [ '' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == ApiErrorType.NO_ANIMAL_FOUND_WITH_SPECIES.value
   assert result.get( 'apiErrorParams' ) == { 'species': ANIMAL_NAME }


def Test_SetAnimalOnDisplay_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_animal_coordinator: StubAnimalCoordinator ) -> None:
   handler = make_handler(
      '/set-animal-on-display',
      {
         'species': ANIMAL_NAME,
         'exhibit': ANIMAL_EXHIBIT,
         'viewingScopes': [ 'Female Herd' ],
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
            'viewing_scopes': [
               AnimalViewingScope.from_enclosure_name( 'Female Herd' ),
            ],
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'species' ] == ANIMAL_NAME
   assert result[ 'exhibit' ] == ANIMAL_EXHIBIT
   assert result[ 'viewingScopes' ] == [
      {
         'enclosureName': 'Female Herd',
         'label': 'Female Herd',
      },
   ]
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
         'viewingScopes': [ '' ],
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
            'viewingScopes': [ 'Female Herd' ],
         },
         ApiErrorType.NO_OFF_DISPLAY_ENTRY_FOUND.value,
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
         ApiErrorType.COULD_NOT_SET_LIMITED_VIEWING_SCHEDULE.value,
      ),
      (
         '/remove-animal-visibility-schedule',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
         },
         ApiErrorType.COULD_NOT_REMOVE_VISIBILITY_SCHEDULE.value,
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
         ApiErrorType.COULD_NOT_SET_VIEWING_ALERT.value,
      ),
      (
         '/remove-animal-viewing-alert',
         {
            'species': ANIMAL_NAME,
            'exhibit': ANIMAL_EXHIBIT,
         },
         ApiErrorType.COULD_NOT_REMOVE_VIEWING_ALERT.value,
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
