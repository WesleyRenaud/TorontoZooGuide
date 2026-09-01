from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_itinerary_coordinator import StubItineraryCoordinator
import pytest

from api import database_connection_provider as connection
import api.http_request_handler as server
from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
import api.request_connection_provider as request_connection
from api.shared.itinerary_config_builder import ItineraryConfigBuilder
from api.types import Types


ANIMAL_EXHIBIT = 'Africa Savanna'
VISIT_DATE = '2026-06-15'

EMPTY_ITINERARY_PATH = {
   'stops': [],
   'legs': [],
   'points': [],
}

EMPTY_ITINERARY = {
   'date': VISIT_DATE,
   'arrival_time': None,
   'departure_time': None,
   'selected_exhibits': [],
   'animals': [],
   'attractions': [],
   'transportations': [],
   'transportation_stations': [],
   'guardians_talks': [],
   'wild_encounters': [],
   'events': [],
}


@pytest.fixture
def stub_itinerary_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubItineraryCoordinator:
   StubItineraryCoordinator.instances = []
   StubItineraryCoordinator.default_success = True
   stub = StubItineraryCoordinator()

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubItineraryCoordinator.instances:
         StubItineraryCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, ItineraryCoordinator, stub )

   return stub


def Test_SetItineraryArrivalTime_TestHttpRequest_ExpectOnlyArrivalUpdated(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   arrival_handler = make_handler(
      '/set-itinerary-arrival-time',
      { 'arrivalTime': '9:45 AM' } )
   departure_handler = make_handler(
      '/set-itinerary-departure-time',
      { 'departureTime': None } )

   server.HttpRequestHandler.do_POST( arrival_handler )
   server.HttpRequestHandler.do_POST( departure_handler )

   assert response_json( arrival_handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'itinerary_config': ItineraryConfigBuilder.to_dict(),
      'itinerary_path': EMPTY_ITINERARY_PATH,
      'itinerary': {
         **EMPTY_ITINERARY,
         'arrival_time': '9:45 AM',
      },
   }
   assert response_json( departure_handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'itinerary_config': ItineraryConfigBuilder.to_dict(),
      'itinerary_path': EMPTY_ITINERARY_PATH,
      'itinerary': EMPTY_ITINERARY,
   }
   assert stub_itinerary_coordinator.calls == [
      (
         'set_arrival_time',
         {
            'arrival_time': '9:45 AM',
            'confirming_short_visit': False,
            'confirming_early_admission': False,
         },
      ),
      (
         'set_departure_time',
         {
            'departure_time': None,
            'confirming_short_visit': False,
         },
      ),
   ]


def Test_SuppressItineraryWarning_TestHttpRequest_ExpectMapsWarningType(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler(
      '/suppress-itinerary-warning',
      { 'warningType': 'arrivalDepartureTooClose' } )

   server.HttpRequestHandler.do_POST( handler )

   assert response_json( handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'itinerary_config': ItineraryConfigBuilder.to_dict(),
   }
   assert stub_itinerary_coordinator.calls == [
      (
         'suppress_itinerary_warning',
         { 'warning_type': 'arrivalDepartureTooClose' },
      ),
   ]


def Test_SetItinerary_TestHttpRequest_ExpectSuccessPayloads(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   set_handler = make_handler(
      '/set-itinerary',
      {
         'date': VISIT_DATE,
         'arrivalTime': '09:30',
         'departureTime': '17:00',
         'selectedExhibits': [ ANIMAL_EXHIBIT ],
         'animals': [],
         'attractions': [],
         'guardiansTalks': [],
         'wildEncounters': [],
      } )
   get_handler = make_handler( '/get-itinerary' )
   clear_handler = make_handler( '/clear-itinerary' )
   accept_handler = make_handler( '/accept-itinerary' )

   server.HttpRequestHandler.do_POST( set_handler )
   server.HttpRequestHandler.do_POST( get_handler )
   server.HttpRequestHandler.do_POST( clear_handler )
   server.HttpRequestHandler.do_POST( accept_handler )

   set_response = response_json( set_handler )
   assert set_response[ 'status' ] == 'success'
   assert set_response[ 'reasons' ] == []
   assert set_response[ 'itinerary_path' ] == EMPTY_ITINERARY_PATH
   assert stub_itinerary_coordinator.calls[ 0 ] == (
      'set_itinerary',
      {
         'date': VISIT_DATE,
         'arrival_time': '09:30',
         'departure_time': '17:00',
         'selected_exhibits': [ ANIMAL_EXHIBIT ],
         'animals': [],
         'attractions': [],
         'transportations': [],
         'guardians_talks': [],
         'wild_encounters': [],
         'visit_date_temp': None,
         'overriding_conflicting_guardians_talks': False,
         'confirming_short_visit': False,
         'confirming_early_admission': False,
         'confirming_guardians_talk_unschedule': False,
         'confirming_wild_encounter_unschedule': False,
         'confirming_fixed_time_item_long_wait': False,
         'confirming_guardians_talk_without_animal': False,
         'confirming_attraction_without_animal': False,
      },
   )
   assert response_json( get_handler )[ 'itinerary' ][ 'date' ] == VISIT_DATE
   assert response_json( get_handler )[ 'itinerary_path' ] == EMPTY_ITINERARY_PATH
   assert response_json( clear_handler )[ 'success' ] is True
   assert response_json( accept_handler )[ 'success' ] is True
   assert response_json( accept_handler )[ 'itinerary' ][ 'date' ] == VISIT_DATE
   assert response_json( accept_handler )[ 'itinerary_path' ] == EMPTY_ITINERARY_PATH
   assert stub_itinerary_coordinator.calls[ -2 ] == (
      'AcceptItineraryProvider.accept_itinerary',
      {
         'animals_to_keep': None,
         'attractions_to_keep': None,
      },
   )


def Test_UnscheduleItineraryItem_TestHttpRequest_ExpectMapsAnimalKey(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler(
      '/unschedule-itinerary-item',
      {
         'itemType': 'animals',
         'key': 'African Lion||Africa Savanna',
      } )

   server.HttpRequestHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'reasons' ] == []
   assert response[ 'itinerary' ] is not None
   assert stub_itinerary_coordinator.calls == [
      (
         'unschedule_itinerary_item',
         {
            'schedule_item_key': AnimalScheduleItemKey(
               species='African Lion',
               exhibit='Africa Savanna' ),
         },
      ),
   ]


def Test_UnscheduleAllItineraryItems_TestHttpRequest_ExpectMapsTemp(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler(
      '/unschedule-all-itinerary-items',
      {
         'temp': True,
      } )

   server.HttpRequestHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'reasons' ] == []
   assert response[ 'itinerary' ] is not None
   assert response[ 'itinerary_config' ] is not None
   assert stub_itinerary_coordinator.calls == [
      (
         'unschedule_all_itinerary_items',
         {
            'visit_date_temp': True,
         },
      ),
   ]


def Test_RemoveItemFromItinerary_TestHttpRequest_ExpectMapsAttractionKey(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler(
      '/remove-item-from-itinerary',
      {
         'itemType': 'attractions',
         'key': 'Conservation Carousel',
      } )

   server.HttpRequestHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'reasons' ] == []
   assert response[ 'itinerary' ] is not None
   assert stub_itinerary_coordinator.calls == [
      (
         'remove_itinerary_item',
         {
            'schedule_item_key': AttractionScheduleItemKey(
               name='Conservation Carousel' ),
         },
      ),
   ]


def Test_AcceptItinerary_TestAnimalsToKeep_ExpectMapsPayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler(
      '/accept-itinerary',
      {
         'temp': 22.5,
         'animalsToKeep': [
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
            },
         ],
      },
   )

   server.HttpRequestHandler.do_POST( handler )

   response = response_json( handler )

   assert response[ 'success' ] is True
   assert response[ 'itinerary' ][ 'date' ] == VISIT_DATE
   assert stub_itinerary_coordinator.calls[ 0 ] == (
      'AcceptItineraryProvider.accept_itinerary',
      {
         'animals_to_keep': [
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
            },
         ],
         'attractions_to_keep': None,
      },
   )
   assert stub_itinerary_coordinator.calls[ 1 ] == (
      'get_itinerary',
      { 'visit_date_temp': 22.5 },
   )


def Test_AcceptItinerary_TestAttractionsToKeep_ExpectMapsPayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler(
      '/accept-itinerary',
      {
         'attractionsToKeep': [ 'Conservation Carousel' ],
      },
   )

   server.HttpRequestHandler.do_POST( handler )

   response = response_json( handler )

   assert response[ 'success' ] is True
   assert stub_itinerary_coordinator.calls[ 0 ] == (
      'AcceptItineraryProvider.accept_itinerary',
      {
         'animals_to_keep': None,
         'attractions_to_keep': [ 'Conservation Carousel' ],
      },
   )


def Test_ScheduleItineraryItem_TestHttpRequest_ExpectMapsPayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler(
      '/schedule-itinerary-item',
      {
         'itemType': 'animals',
         'key': 'African Lion||Africa Savanna',
         'startTime': '14:00',
         'durationMinutes': 20,
         'confirmingScheduleItemNotOnItinerary': True,
         'confirmingAttractionOutsideOperatingHours': True,
         'confirmingGuardiansTalkUnschedule': True,
         'confirmingWildEncounterUnschedule': True,
         'confirmingFixedTimeItemLongWait': True,
         'confirmingGuardiansTalkWithoutAnimal': True,
      } )

   server.HttpRequestHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'itinerary' ] is not None
   assert stub_itinerary_coordinator.calls == [
      (
         'schedule_itinerary_item',
         {
            'schedule_item_key': AnimalScheduleItemKey(
               species='African Lion',
               exhibit='Africa Savanna' ),
            'start_time': '14:00',
            'duration_minutes': 20,
            'confirming_schedule_item_not_on_itinerary': True,
            'confirming_attraction_outside_operating_hours': True,
            'confirming_guardians_talk_unschedule': True,
            'confirming_wild_encounter_unschedule': True,
            'confirming_fixed_time_item_long_wait': True,
            'confirming_guardians_talk_without_animal': True,
         },
      ),
   ]


def Test_BulkScheduleItinerary_TestHttpRequest_ExpectMapsPayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler(
      '/bulk-schedule-itinerary',
      {
         'temp': 22.5,
         'confirmingFixedTimeItemLongWait': True,
      } )

   server.HttpRequestHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'itinerary' ] is not None
   assert stub_itinerary_coordinator.calls == [
      (
         'bulk_schedule_itinerary',
         {
            'visit_date_temp': 22.5,
            'confirming_fixed_time_item_long_wait': True,
         },
      ),
   ]


def Test_GetItineraryDate_TestHttpRequest_ExpectDatePayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler( '/get-itinerary-date', {} )

   server.HttpRequestHandler.do_POST( handler )

   assert response_json( handler ) == { 'date': VISIT_DATE }
   assert stub_itinerary_coordinator.calls == [
      ( 'get_itinerary_date', {} ),
   ]


def Test_SetItineraryDepartureTime_TestHttpRequest_ExpectMappedDeparture(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler(
      '/set-itinerary-departure-time',
      {
         'departureTime': '16:30',
         'confirmingShortVisit': True,
      } )

   server.HttpRequestHandler.do_POST( handler )

   assert response_json( handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'itinerary_config': ItineraryConfigBuilder.to_dict(),
      'itinerary_path': EMPTY_ITINERARY_PATH,
      'itinerary': {
         **EMPTY_ITINERARY,
         'departure_time': '16:30',
      },
   }
   assert stub_itinerary_coordinator.calls == [
      (
         'set_departure_time',
         {
            'departure_time': '16:30',
            'confirming_short_visit': True,
         },
      ),
   ]
