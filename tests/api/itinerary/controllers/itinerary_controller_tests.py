from __future__ import annotations

from typing import Any

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
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.domain.itinerary_adjustment import ItineraryAdjustment
from api.itinerary.domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from api.itinerary.operations.suppress_itinerary_warning_result import SuppressItineraryWarningResult
from api.itinerary.results.itinerary_path_builder import ItineraryPathBuilder
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.results.itinerary_save_result_response_builder import ItinerarySaveResultResponseBuilder
from api.itinerary.results.itinerary_time_set_result import ItineraryTimeSetResult
from api.itinerary.results.itinerary_time_set_result_response_builder import ItineraryTimeSetResultResponseBuilder
from api.itinerary.results.suppress_itinerary_warning_result_response_builder import SuppressItineraryWarningResultResponseBuilder
from api.itinerary.scheduling.items.schedule_item_key_mapper import ScheduleItemKeyMapper
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.models import Itinerary
import api.request_connection_provider as request_connection
from api.shared.api_error_response_applier import ApiErrorResponseApplier
from api.shared.enums import ItineraryAdjustmentType
from api.shared.enums import ItineraryErrorType, Position
from api.shared.enums.api_error_type import ApiErrorType
from api.shared.enums.schedule_item_kind import ScheduleItemKind
from api.shared.itinerary_config_builder import ItineraryConfigBuilder
from api.types import Types


ANIMAL_EXHIBIT = 'Africa Savanna'
ANIMAL_SPECIES = 'African Lion'
ATTRACTION_NAME = 'Conservation Carousel'
VISIT_DATE = '2026-06-15'
VISIT_DATE_TEMP = 22.5
WARNING_TYPE = 'arrivalDepartureTooClose'


def _post_json( handler: server.HttpRequestHandler ) -> dict[ str, Any ]:
   server.HttpRequestHandler.do_POST( handler )
   return response_json( handler )


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
         StubItineraryCoordinator.instances[ Position.LAST ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, ItineraryCoordinator, stub )

   return stub


def Test_SetItineraryArrivalTime_TestHttpRequest_ExpectOnlyArrivalUpdated(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   arrival_time = '9:45 AM'
   confirming_short_visit = False
   confirming_early_admission = False
   expected_result = ItineraryTimeSetResult(
      itinerary=Itinerary(
         date=VISIT_DATE,
         arrival_time=arrival_time ) )
   handler = make_handler(
      '/set-itinerary-arrival-time',
      { 'arrivalTime': arrival_time } )

   result = _post_json( handler )

   assert result == ItineraryTimeSetResultResponseBuilder.to_dict( expected_result )
   assert stub_itinerary_coordinator.calls == [
      (
         'set_arrival_time',
         {
            'arrival_time': arrival_time,
            'confirming_short_visit': confirming_short_visit,
            'confirming_early_admission': confirming_early_admission,
         },
      ),
   ]


def Test_SetItineraryDepartureTime_TestClearedTime_ExpectEmptyItinerary(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   departure_time = None
   confirming_short_visit = False
   expected_result = ItineraryTimeSetResult(
      itinerary=Itinerary(
         date=VISIT_DATE,
         departure_time=departure_time ) )
   handler = make_handler(
      '/set-itinerary-departure-time',
      { 'departureTime': departure_time } )

   result = _post_json( handler )

   assert result == ItineraryTimeSetResultResponseBuilder.to_dict( expected_result )
   assert stub_itinerary_coordinator.calls == [
      (
         'set_departure_time',
         {
            'departure_time': departure_time,
            'confirming_short_visit': confirming_short_visit,
         },
      ),
   ]


def Test_SuppressItineraryWarning_TestHttpRequest_ExpectMapsWarningType(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   expected_result = SuppressItineraryWarningResult()
   handler = make_handler(
      '/suppress-itinerary-warning',
      { 'warningType': WARNING_TYPE } )

   result = _post_json( handler )

   assert result == SuppressItineraryWarningResultResponseBuilder.to_dict(
      expected_result )
   assert stub_itinerary_coordinator.calls == [
      (
         'suppress_itinerary_warning',
         { 'warning_type': WARNING_TYPE },
      ),
   ]


def Test_UnsuppressItineraryWarning_TestHttpRequest_ExpectMapsWarningType(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   expected_result = SuppressItineraryWarningResult()
   handler = make_handler(
      '/unsuppress-itinerary-warning',
      { 'warningType': WARNING_TYPE } )

   result = _post_json( handler )

   assert result == SuppressItineraryWarningResultResponseBuilder.to_dict(
      expected_result )
   assert stub_itinerary_coordinator.calls == [
      (
         'unsuppress_itinerary_warning',
         { 'warning_type': WARNING_TYPE },
      ),
   ]


def Test_SetItinerary_TestHttpRequest_ExpectSuccessPayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   arrival_time = '09:30'
   departure_time = '17:00'
   selected_exhibits = [ ANIMAL_EXHIBIT ]
   animals: list[ object ] = []
   attractions: list[ object ] = []
   guardians_talks: list[ object ] = []
   wild_encounters: list[ object ] = []
   save_result = ItinerarySaveResult( itinerary=Itinerary( date=VISIT_DATE ) )
   handler = make_handler(
      '/set-itinerary',
      {
         'date': VISIT_DATE,
         'arrivalTime': arrival_time,
         'departureTime': departure_time,
         'selectedExhibits': selected_exhibits,
         'animals': animals,
         'attractions': attractions,
         'guardiansTalks': guardians_talks,
         'wildEncounters': wild_encounters,
      } )

   result = _post_json( handler )

   assert result == ItinerarySaveResultResponseBuilder.to_dict(
      save_result,
      include_config=True )
   assert stub_itinerary_coordinator.calls == [
      (
         'set_itinerary',
         {
            'date': VISIT_DATE,
            'arrival_time': arrival_time,
            'departure_time': departure_time,
            'selected_exhibits': selected_exhibits,
            'animals': animals,
            'attractions': attractions,
            'transportations': ItineraryTransportationInput.from_wires( None ),
            'guardians_talks': guardians_talks,
            'wild_encounters': WildEncounterScheduleItemKey.from_wires(
               wild_encounters ),
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
      ),
   ]


def Test_GetItinerary_TestHttpRequest_ExpectItinerary(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   itinerary = Itinerary( date=VISIT_DATE )
   handler = make_handler( '/get-itinerary' )

   result = _post_json( handler )

   assert result[ 'itinerary' ] == itinerary.to_dict()
   assert result[ 'itinerary_path' ] == ItineraryPathBuilder.build( None )
   assert result[ 'itinerary_config' ] == ItineraryConfigBuilder.to_dict()
   assert stub_itinerary_coordinator.calls == [
      (
         'get_itinerary',
         { 'visit_date_temp': None },
      ),
   ]


def Test_ClearItinerary_TestHttpRequest_ExpectCleared(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler( '/clear-itinerary' )

   result = _post_json( handler )

   assert result[ 'success' ] is StubItineraryCoordinator.default_success
   assert stub_itinerary_coordinator.calls == [
      ( 'ClearItineraryProvider.clear_itinerary', {} ),
   ]


def Test_AcceptItinerary_TestHttpRequest_ExpectAccepted(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   itinerary = Itinerary( date=VISIT_DATE )
   animals_to_keep = None
   attractions_to_keep = None
   handler = make_handler( '/accept-itinerary' )

   result = _post_json( handler )

   assert result[ 'success' ] is StubItineraryCoordinator.default_success
   assert result[ 'itinerary' ] == itinerary.to_dict()
   assert result[ 'itinerary_path' ] == ItineraryPathBuilder.build( None )
   assert result[ 'itinerary_config' ] == ItineraryConfigBuilder.to_dict()
   assert stub_itinerary_coordinator.calls[ Position.FIRST ] == (
      'AcceptItineraryProvider.accept_itinerary',
      {
         'animals_to_keep': animals_to_keep,
         'attractions_to_keep': attractions_to_keep,
      },
   )
   assert stub_itinerary_coordinator.calls[ Position.SECOND ] == (
      'get_itinerary',
      { 'visit_date_temp': None },
   )


def Test_UnscheduleItineraryItem_TestHttpRequest_ExpectMapsAnimalKey(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   item_type = ScheduleItemKind.ANIMAL.item_type
   key = AnimalScheduleItemKey.wire( ANIMAL_SPECIES, ANIMAL_EXHIBIT )
   save_result = ItinerarySaveResult( itinerary=Itinerary( date=VISIT_DATE ) )
   handler = make_handler(
      '/unschedule-itinerary-item',
      {
         'itemType': item_type,
         'key': key,
      } )

   result = _post_json( handler )

   assert result == ItinerarySaveResultResponseBuilder.to_dict( save_result )
   assert stub_itinerary_coordinator.calls == [
      (
         'unschedule_itinerary_item',
         {
            'schedule_item_key': ScheduleItemKeyMapper.from_wire( item_type, key ),
         },
      ),
   ]


def Test_UnscheduleAllItineraryItems_TestHttpRequest_ExpectMapsTemp(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   visit_date_temp = True
   save_result = ItinerarySaveResult( itinerary=Itinerary( date=VISIT_DATE ) )
   handler = make_handler(
      '/unschedule-all-itinerary-items',
      {
         'temp': visit_date_temp,
      } )

   result = _post_json( handler )

   assert result == ItinerarySaveResultResponseBuilder.to_dict(
      save_result,
      include_config=True )
   assert stub_itinerary_coordinator.calls == [
      (
         'unschedule_all_itinerary_items',
         {
            'visit_date_temp': visit_date_temp,
         },
      ),
   ]


def Test_RemoveItemFromItinerary_TestHttpRequest_ExpectMapsAttractionKey(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   item_type = ScheduleItemKind.ATTRACTION.item_type
   key = AttractionScheduleItemKey( name=ATTRACTION_NAME ).to_wire()
   save_result = ItinerarySaveResult( itinerary=Itinerary( date=VISIT_DATE ) )
   handler = make_handler(
      '/remove-item-from-itinerary',
      {
         'itemType': item_type,
         'key': key,
      } )

   result = _post_json( handler )

   assert result == ItinerarySaveResultResponseBuilder.to_dict( save_result )
   assert stub_itinerary_coordinator.calls == [
      (
         'remove_itinerary_item',
         {
            'schedule_item_key': ScheduleItemKeyMapper.from_wire( item_type, key ),
         },
      ),
   ]


def Test_AcceptItinerary_TestAnimalsToKeep_ExpectMapsPayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   visit_date_temp = VISIT_DATE_TEMP
   animals_to_keep = [
      {
         'species': ANIMAL_SPECIES,
         'exhibit': ANIMAL_EXHIBIT,
      },
   ]
   attractions_to_keep = None
   itinerary = Itinerary( date=VISIT_DATE )
   handler = make_handler(
      '/accept-itinerary',
      {
         'temp': visit_date_temp,
         'animalsToKeep': animals_to_keep,
      },
   )

   result = _post_json( handler )

   assert result[ 'success' ] is StubItineraryCoordinator.default_success
   assert result[ 'itinerary' ][ 'date' ] == itinerary.date
   assert stub_itinerary_coordinator.calls[ Position.FIRST ] == (
      'AcceptItineraryProvider.accept_itinerary',
      {
         'animals_to_keep': animals_to_keep,
         'attractions_to_keep': attractions_to_keep,
      },
   )
   assert stub_itinerary_coordinator.calls[ Position.SECOND ] == (
      'get_itinerary',
      { 'visit_date_temp': visit_date_temp },
   )


def Test_AcceptItinerary_TestAttractionsToKeep_ExpectMapsPayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   attractions_to_keep = [ ATTRACTION_NAME ]
   animals_to_keep = None
   handler = make_handler(
      '/accept-itinerary',
      {
         'attractionsToKeep': attractions_to_keep,
      },
   )

   result = _post_json( handler )

   assert result[ 'success' ] is StubItineraryCoordinator.default_success
   assert stub_itinerary_coordinator.calls[ Position.FIRST ] == (
      'AcceptItineraryProvider.accept_itinerary',
      {
         'animals_to_keep': animals_to_keep,
         'attractions_to_keep': attractions_to_keep,
      },
   )


def Test_ScheduleItineraryItem_TestHttpRequest_ExpectMapsPayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   item_type = ScheduleItemKind.ANIMAL.item_type
   key = AnimalScheduleItemKey.wire( ANIMAL_SPECIES, ANIMAL_EXHIBIT )
   start_time = '14:00'
   duration_minutes = 20
   confirming_schedule_item_not_on_itinerary = True
   confirming_attraction_outside_operating_hours = True
   confirming_guardians_talk_unschedule = True
   confirming_wild_encounter_unschedule = True
   confirming_fixed_time_item_long_wait = True
   confirming_guardians_talk_without_animal = True
   save_result = ItinerarySaveResult( itinerary=Itinerary( date=VISIT_DATE ) )
   handler = make_handler(
      '/schedule-itinerary-item',
      {
         'itemType': item_type,
         'key': key,
         'startTime': start_time,
         'durationMinutes': duration_minutes,
         'confirmingScheduleItemNotOnItinerary': confirming_schedule_item_not_on_itinerary,
         'confirmingAttractionOutsideOperatingHours': confirming_attraction_outside_operating_hours,
         'confirmingGuardiansTalkUnschedule': confirming_guardians_talk_unschedule,
         'confirmingWildEncounterUnschedule': confirming_wild_encounter_unschedule,
         'confirmingFixedTimeItemLongWait': confirming_fixed_time_item_long_wait,
         'confirmingGuardiansTalkWithoutAnimal': confirming_guardians_talk_without_animal,
      } )

   result = _post_json( handler )

   assert result == ItinerarySaveResultResponseBuilder.to_dict(
      save_result,
      include_config=True )
   assert stub_itinerary_coordinator.calls == [
      (
         'schedule_itinerary_item',
         {
            'schedule_item_key': ScheduleItemKeyMapper.from_wire( item_type, key ),
            'start_time': start_time,
            'duration_minutes': duration_minutes,
            'confirming_schedule_item_not_on_itinerary': confirming_schedule_item_not_on_itinerary,
            'confirming_attraction_outside_operating_hours': confirming_attraction_outside_operating_hours,
            'confirming_guardians_talk_unschedule': confirming_guardians_talk_unschedule,
            'confirming_wild_encounter_unschedule': confirming_wild_encounter_unschedule,
            'confirming_fixed_time_item_long_wait': confirming_fixed_time_item_long_wait,
            'confirming_guardians_talk_without_animal': confirming_guardians_talk_without_animal,
         },
      ),
   ]


def Test_BulkScheduleItinerary_TestHttpRequest_ExpectMapsPayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   visit_date_temp = VISIT_DATE_TEMP
   confirming_fixed_time_item_long_wait = True
   save_result = ItinerarySaveResult( itinerary=Itinerary( date=VISIT_DATE ) )
   handler = make_handler(
      '/bulk-schedule-itinerary',
      {
         'temp': visit_date_temp,
         'confirmingFixedTimeItemLongWait': confirming_fixed_time_item_long_wait,
      } )

   result = _post_json( handler )

   assert result == ItinerarySaveResultResponseBuilder.to_dict(
      save_result,
      include_config=True )
   assert stub_itinerary_coordinator.calls == [
      (
         'bulk_schedule_itinerary',
         {
            'visit_date_temp': visit_date_temp,
            'confirming_fixed_time_item_long_wait': confirming_fixed_time_item_long_wait,
         },
      ),
   ]


def Test_GetItineraryDate_TestHttpRequest_ExpectDatePayload(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   handler = make_handler( '/get-itinerary-date', {} )

   result = _post_json( handler )

   assert result == { 'date': VISIT_DATE }
   assert stub_itinerary_coordinator.calls == [
      ( 'get_itinerary_date', {} ),
   ]


def Test_SetItineraryDepartureTime_TestHttpRequest_ExpectMappedDeparture(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   departure_time = '16:30'
   confirming_short_visit = True
   expected_result = ItineraryTimeSetResult(
      itinerary=Itinerary(
         date=VISIT_DATE,
         departure_time=departure_time ) )
   handler = make_handler(
      '/set-itinerary-departure-time',
      {
         'departureTime': departure_time,
         'confirmingShortVisit': confirming_short_visit,
      } )

   result = _post_json( handler )

   assert result == ItineraryTimeSetResultResponseBuilder.to_dict( expected_result )
   assert stub_itinerary_coordinator.calls == [
      (
         'set_departure_time',
         {
            'departure_time': departure_time,
            'confirming_short_visit': confirming_short_visit,
         },
      ),
   ]


def Test_GetItinerary_TestHttpRequest_ExpectMapsTemp(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   visit_date_temp = VISIT_DATE_TEMP
   itinerary = Itinerary( date=VISIT_DATE )
   handler = make_handler(
      '/get-itinerary',
      {
         'temp': visit_date_temp,
      } )

   result = _post_json( handler )

   assert result[ 'itinerary' ][ 'date' ] == itinerary.date
   assert result[ 'itinerary_path' ] == ItineraryPathBuilder.build( None )
   assert result[ 'itinerary_config' ] == ItineraryConfigBuilder.to_dict()
   assert stub_itinerary_coordinator.calls == [
      (
         'get_itinerary',
         {
            'visit_date_temp': visit_date_temp,
         },
      ),
   ]


def Test_ClearItinerary_TestHttpRequest_ExpectCouldNotClearApiError(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   StubItineraryCoordinator.default_success = False
   expected = { 'success': StubItineraryCoordinator.default_success }
   ApiErrorResponseApplier.apply_error(
      expected,
      ApiErrorType.COULD_NOT_CLEAR_ITINERARY )
   handler = make_handler( '/clear-itinerary' )

   result = _post_json( handler )

   assert result == expected
   assert stub_itinerary_coordinator.calls == [
      ( 'ClearItineraryProvider.clear_itinerary', {} ),
   ]


def Test_AcceptItinerary_TestHttpRequest_ExpectCouldNotAcceptApiError(
      stub_itinerary_coordinator: StubItineraryCoordinator ) -> None:
   StubItineraryCoordinator.default_success = False
   animals_to_keep = None
   attractions_to_keep = None
   expected = {
      'success': StubItineraryCoordinator.default_success,
      'itinerary': None,
      'itinerary_config': ItineraryConfigBuilder.to_dict(),
      'itinerary_path': ItineraryPathBuilder.build( None ),
   }
   ApiErrorResponseApplier.apply_error(
      expected,
      ApiErrorType.COULD_NOT_ACCEPT_ITINERARY_CHANGES )
   handler = make_handler( '/accept-itinerary' )

   result = _post_json( handler )

   assert result == expected
   assert stub_itinerary_coordinator.calls == [
      (
         'AcceptItineraryProvider.accept_itinerary',
         {
            'animals_to_keep': animals_to_keep,
            'attractions_to_keep': attractions_to_keep,
         },
      ),
   ]


def Test_SetItinerary_TestSaveResultAdjustments_ExpectResponseAdjustments(
      stub_itinerary_coordinator: StubItineraryCoordinator,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   visit_date = '2026-06-22'
   requested_arrival_time = '09:15'
   previous_arrival_time = '9:15 AM'
   adjusted_arrival_value = '09:30'
   itinerary_arrival_time = '9:30 AM'
   departure_time = '17:00'
   animals: list[ object ] = []
   attractions: list[ object ] = []
   transportations: list[ object ] = []
   guardians_talks: list[ object ] = []
   wild_encounters: list[ object ] = []
   adjustment = ItineraryAdjustment(
      type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
      field='arrivalTime',
      previous_value=previous_arrival_time,
      value=adjusted_arrival_value,
      reason=ItineraryAdjustmentReason.ARRIVAL_OUTSIDE_ADMISSION_HOURS,
   )
   save_result = ItinerarySaveResult(
      status=ItineraryErrorType.SUCCESS,
      itinerary=Itinerary(
         date=visit_date,
         arrival_time=itinerary_arrival_time,
      ),
      adjustments=[ adjustment ],
   )

   def stub_set_itinerary( **kwargs: Any ) -> ItinerarySaveResult:
      stub_itinerary_coordinator.calls.append( ( 'set_itinerary', kwargs ) )
      return save_result

   monkeypatch.setattr( ItineraryCoordinator, 'set_itinerary', stub_set_itinerary )
   handler = make_handler(
      '/set-itinerary',
      {
         'date': visit_date,
         'arrivalTime': requested_arrival_time,
         'departureTime': departure_time,
         'animals': animals,
         'attractions': attractions,
         'transportations': transportations,
         'guardiansTalks': guardians_talks,
         'wildEncounters': wild_encounters,
      } )

   result = _post_json( handler )

   assert result == ItinerarySaveResultResponseBuilder.to_dict(
      save_result,
      include_config=True )
