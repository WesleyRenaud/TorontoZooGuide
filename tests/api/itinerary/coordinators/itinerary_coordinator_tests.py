from __future__ import annotations

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.itinerary.conflicts.visit_window_overflow_issue_finder import VisitWindowOverflowIssueFinder
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.accept_itinerary_provider import AcceptItineraryProvider
from api.itinerary.data_access.clear_itinerary_provider import ClearItineraryProvider
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.data_access.itinerary_save_input_mapper import ItinerarySaveInputMapper
from api.itinerary.data_access.itinerary_time_provider import ItineraryTimeProvider
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder
from api.itinerary.operations.all_itinerary_items_unscheduler import AllItineraryItemsUnscheduler
from api.itinerary.operations.itinerary_item_remover import ItineraryItemRemover
from api.itinerary.operations.itinerary_item_unscheduler import ItineraryItemUnscheduler
from api.itinerary.operations.itinerary_setter import ItinerarySetter
from api.itinerary.operations.itinerary_warning_suppressor import ItineraryWarningSuppressor
from api.itinerary.operations.suppress_itinerary_warning_result import SuppressItineraryWarningResult
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner import BulkScheduleItineraryRunner
from api.itinerary.scheduling.bulk.bulk_schedule_stop_selector import BulkScheduleStopSelector
from api.itinerary.scheduling.items.itinerary_item_scheduler import ItineraryItemScheduler
from api.itinerary.scheduling.items.schedule_item_key import ScheduleItemKey
from api.itinerary.validation.fixed_zoo_schedule_start_times_builder import FixedZooScheduleStartTimesBuilder
from api.itinerary.validation.itinerary_arrival_time_validator import ItineraryArrivalTimeValidator
from api.itinerary.validation.itinerary_departure_time_validator import ItineraryDepartureTimeValidator
from api.itinerary.warnings.early_admission_warning_builder import EarlyAdmissionWarningBuilder
from api.itinerary.warnings.short_visit_warning_builder import ShortVisitWarningBuilder
from api.models import Itinerary
from api.shared.enums import ItineraryErrorType
from api.types import Types
from api.zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider


ITINERARY_DATE = '2026-06-15'
ARRIVAL_TIME = '10:00 AM'
DEPARTURE_TIME = '4:00 PM'
WARNING_TYPE = 'arrivalDepartureTooClose'
VISIT_DATE_TEMP = 22.0
LION_SPECIES = 'African Lion'
LION_EXHIBIT = 'Africa Savanna'
CAROUSEL = 'Conservation Carousel'

ITINERARY = Itinerary(
   date=ITINERARY_DATE,
   arrival_time=ARRIVAL_TIME,
   departure_time=DEPARTURE_TIME )
SAVE_RESULT = ItinerarySaveResult( itinerary=ITINERARY )
SAVED_ITINERARY = SavedItinerary(
   date_value=ITINERARY_DATE,
   arrival_time=ARRIVAL_TIME,
   departure_time=DEPARTURE_TIME )
ZOO_HOURS_RECORD = object()


def Test_GetItineraryDate_TestProviderDate_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )

   itinerary_date = ItineraryCoordinator.get_itinerary_date()

   assert itinerary_date == ITINERARY_DATE


def Test_GetItinerary_TestBuilder_ExpectItinerary(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )

   def build_current( **kwargs: object ) -> Itinerary:
      captured.update( kwargs )
      return ITINERARY

   monkeypatch.setattr( ItineraryBuilder, 'build_current', build_current )

   itinerary = ItineraryCoordinator.get_itinerary( visit_date_temp=VISIT_DATE_TEMP )

   assert itinerary is ITINERARY
   assert captured[ 'saved_itinerary' ] is SAVED_ITINERARY
   assert captured[ 'visit_date_temp' ] == VISIT_DATE_TEMP


def Test_SetItinerary_TestSetter_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}
   animals = [ { 'species': LION_SPECIES, 'exhibit': LION_EXHIBIT } ]
   confirming_short_visit = True

   def set_itinerary( conn: Types.Connection, **kwargs: object ) -> ItinerarySaveResult:
      captured[ 'conn' ] = conn
      captured[ 'kwargs' ] = kwargs
      return SAVE_RESULT

   monkeypatch.setattr( ItinerarySetter, 'set', set_itinerary )

   result = ItineraryCoordinator.set_itinerary(
      date=ITINERARY_DATE,
      animals=animals,
      confirming_short_visit=confirming_short_visit )

   assert result is SAVE_RESULT
   assert captured[ 'conn' ] is STUB_REQUEST_CONNECTION
   assert captured[ 'kwargs' ][ 'date' ] == ITINERARY_DATE
   assert captured[ 'kwargs' ][ 'confirming_short_visit' ] is confirming_short_visit


def Test_ScheduleItineraryItem_TestScheduler_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   schedule_key: ScheduleItemKey.Key | None = None
   captured: dict[ str, object ] = {}
   confirming_fixed_time_item_long_wait = True

   def schedule(
         conn: Types.Connection,
         key: ScheduleItemKey.Key | None,
         **kwargs: object ) -> ItinerarySaveResult:
      captured[ 'conn' ] = conn
      captured[ 'key' ] = key
      captured[ 'kwargs' ] = kwargs
      return SAVE_RESULT

   monkeypatch.setattr( ItineraryItemScheduler, 'schedule', schedule )

   result = ItineraryCoordinator.schedule_itinerary_item(
      schedule_key,
      start_time=ARRIVAL_TIME,
      confirming_fixed_time_item_long_wait=confirming_fixed_time_item_long_wait )

   assert result is SAVE_RESULT
   assert captured[ 'conn' ] is STUB_REQUEST_CONNECTION
   assert captured[ 'key' ] is schedule_key
   assert captured[ 'kwargs' ][ 'start_time' ] == ARRIVAL_TIME
   assert captured[ 'kwargs' ][ 'confirming_fixed_time_item_long_wait' ] is confirming_fixed_time_item_long_wait


def Test_BulkScheduleItinerary_TestRunner_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   stops = [ object() ]
   captured: dict[ str, object ] = {}
   confirming_fixed_time_item_long_wait = True

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      BulkScheduleStopSelector,
      'stops',
      lambda saved, *, only_previously_scheduled: stops
      if saved is SAVED_ITINERARY and only_previously_scheduled is False
      else [] )

   def run( conn: Types.Connection, **kwargs: object ) -> ItinerarySaveResult:
      captured[ 'conn' ] = conn
      captured[ 'kwargs' ] = kwargs
      return SAVE_RESULT

   monkeypatch.setattr( BulkScheduleItineraryRunner, 'run', run )

   result = ItineraryCoordinator.bulk_schedule_itinerary(
      visit_date_temp=VISIT_DATE_TEMP,
      confirming_fixed_time_item_long_wait=confirming_fixed_time_item_long_wait )

   assert result is SAVE_RESULT
   assert captured[ 'conn' ] is STUB_REQUEST_CONNECTION
   assert captured[ 'kwargs' ][ 'stops_to_schedule' ] is stops
   assert captured[ 'kwargs' ][ 'visit_date_temp' ] == VISIT_DATE_TEMP
   assert captured[ 'kwargs' ][ 'confirming_fixed_time_item_long_wait' ] is confirming_fixed_time_item_long_wait


def Test_ClearItinerary_TestProvider_ExpectCleared(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ClearItineraryProvider,
      'clear_itinerary',
      lambda conn: conn is STUB_REQUEST_CONNECTION )

   cleared = ItineraryCoordinator.clear_itinerary()

   assert cleared is True


def Test_UnscheduleAllItineraryItems_TestUnscheduler_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   def unschedule_all( conn: Types.Connection, **kwargs: object ) -> ItinerarySaveResult:
      captured[ 'conn' ] = conn
      captured[ 'kwargs' ] = kwargs
      return SAVE_RESULT

   monkeypatch.setattr(
      AllItineraryItemsUnscheduler,
      'unschedule_all',
      unschedule_all )

   result = ItineraryCoordinator.unschedule_all_itinerary_items(
      visit_date_temp=VISIT_DATE_TEMP )

   assert result is SAVE_RESULT
   assert captured[ 'conn' ] is STUB_REQUEST_CONNECTION
   assert captured[ 'kwargs' ][ 'visit_date_temp' ] == VISIT_DATE_TEMP


def Test_UnscheduleItineraryItem_TestUnscheduler_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   schedule_key: ScheduleItemKey.Key | None = None
   captured: dict[ str, object ] = {}

   def unschedule(
         conn: Types.Connection,
         key: ScheduleItemKey.Key | None ) -> ItinerarySaveResult:
      captured[ 'conn' ] = conn
      captured[ 'key' ] = key
      return SAVE_RESULT

   monkeypatch.setattr( ItineraryItemUnscheduler, 'unschedule', unschedule )

   result = ItineraryCoordinator.unschedule_itinerary_item( schedule_key )

   assert result is SAVE_RESULT
   assert captured[ 'conn' ] is STUB_REQUEST_CONNECTION
   assert captured[ 'key' ] is schedule_key


def Test_RemoveItineraryItem_TestRemover_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   schedule_key: ScheduleItemKey.Key | None = None
   captured: dict[ str, object ] = {}

   def remove(
         conn: Types.Connection,
         key: ScheduleItemKey.Key | None ) -> ItinerarySaveResult:
      captured[ 'conn' ] = conn
      captured[ 'key' ] = key
      return SAVE_RESULT

   monkeypatch.setattr( ItineraryItemRemover, 'remove', remove )

   result = ItineraryCoordinator.remove_itinerary_item( schedule_key )

   assert result is SAVE_RESULT
   assert captured[ 'conn' ] is STUB_REQUEST_CONNECTION
   assert captured[ 'key' ] is schedule_key


def Test_SuppressItineraryWarning_TestSuppressor_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   expected = SuppressItineraryWarningResult()
   captured: dict[ str, object ] = {}

   def suppress(
         conn: Types.Connection,
         warning_type: str ) -> SuppressItineraryWarningResult:
      captured[ 'conn' ] = conn
      captured[ 'warning_type' ] = warning_type
      return expected

   monkeypatch.setattr( ItineraryWarningSuppressor, 'suppress', suppress )

   result = ItineraryCoordinator.suppress_itinerary_warning( WARNING_TYPE )

   assert result is expected
   assert captured[ 'conn' ] is STUB_REQUEST_CONNECTION
   assert captured[ 'warning_type' ] == WARNING_TYPE


def Test_UnsuppressItineraryWarning_TestSuppressor_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   expected = SuppressItineraryWarningResult()
   captured: dict[ str, object ] = {}

   def unsuppress(
         conn: Types.Connection,
         warning_type: str ) -> SuppressItineraryWarningResult:
      captured[ 'conn' ] = conn
      captured[ 'warning_type' ] = warning_type
      return expected

   monkeypatch.setattr( ItineraryWarningSuppressor, 'unsuppress', unsuppress )

   result = ItineraryCoordinator.unsuppress_itinerary_warning( WARNING_TYPE )

   assert result is expected
   assert captured[ 'conn' ] is STUB_REQUEST_CONNECTION
   assert captured[ 'warning_type' ] == WARNING_TYPE


def Test_AcceptItinerary_TestProvider_ExpectMappedKeepLists(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animals_to_keep = [ { 'species': LION_SPECIES, 'exhibit': LION_EXHIBIT } ]
   attractions_to_keep = [ CAROUSEL ]
   mapped_animals = [ object() ]
   mapped_attractions = [ CAROUSEL ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      ItinerarySaveInputMapper,
      'map_animal_inputs',
      lambda animals: mapped_animals if animals is animals_to_keep else [] )
   monkeypatch.setattr(
      ItinerarySaveInputMapper,
      'map_named_strings',
      lambda names: mapped_attractions if names is attractions_to_keep else [] )

   def accept(
         conn: Types.Connection,
         *,
         animals_to_keep: list[ ItineraryAnimalInput ] | None = None,
         attractions_to_keep: list[ str ] | None = None ) -> bool:
      captured[ 'conn' ] = conn
      captured[ 'animals' ] = animals_to_keep
      captured[ 'attractions' ] = attractions_to_keep
      return True

   monkeypatch.setattr( AcceptItineraryProvider, 'accept_itinerary', accept )

   accepted = ItineraryCoordinator.accept_itinerary(
      animals_to_keep=animals_to_keep,
      attractions_to_keep=attractions_to_keep )

   assert accepted is True
   assert captured[ 'conn' ] is STUB_REQUEST_CONNECTION
   assert captured[ 'animals' ] is mapped_animals
   assert captured[ 'attractions' ] is mapped_attractions


def Test_SetArrivalTime_TestClearedTime_ExpectClearsAndReturnsItinerary(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   arrival_time = None
   cleared: list[ object ] = []
   cleared_schedules: list[ object ] = []

   monkeypatch.setattr(
      ItineraryTimeProvider,
      'set_itinerary_arrival_time',
      lambda conn, value: cleared.append( ( conn, value ) ) )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryVisitWindowBuilder,
      'clear_schedules_outside',
      lambda conn, *, arrival_time, departure_time: cleared_schedules.append(
         ( conn, arrival_time, departure_time ) ) )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda *_args, **_kwargs: ITINERARY )

   result = ItineraryCoordinator.set_arrival_time( arrival_time )

   assert result.success is True
   assert result.itinerary is ITINERARY
   assert cleared == [ ( STUB_REQUEST_CONNECTION, arrival_time ) ]
   assert cleared_schedules == [
      (
         STUB_REQUEST_CONNECTION,
         SAVED_ITINERARY.arrival_time,
         SAVED_ITINERARY.departure_time,
      ),
   ]


def Test_SetArrivalTime_TestValidationFailure_ExpectStatusOnly(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validation_error = ItineraryErrorType.TIME_OUT_OF_BOUNDS

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda *_args, **_kwargs: ZOO_HOURS_RECORD )
   monkeypatch.setattr(
      FixedZooScheduleStartTimesBuilder,
      'from_saved_itinerary',
      lambda _saved: [] )
   monkeypatch.setattr(
      ItineraryArrivalTimeValidator,
      'validate_for_zoo_hours',
      lambda *_args, **_kwargs: validation_error )

   result = ItineraryCoordinator.set_arrival_time( ARRIVAL_TIME )

   assert result.status == validation_error
   assert result.itinerary is None


def Test_SetArrivalTime_TestEarlyAdmissionWarning_ExpectMembershipStatus(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda *_args, **_kwargs: ZOO_HOURS_RECORD )
   monkeypatch.setattr(
      FixedZooScheduleStartTimesBuilder,
      'from_saved_itinerary',
      lambda _saved: [] )
   monkeypatch.setattr(
      ItineraryArrivalTimeValidator,
      'validate_for_zoo_hours',
      lambda *_args, **_kwargs: ItineraryErrorType.SUCCESS )
   monkeypatch.setattr(
      EarlyAdmissionWarningBuilder,
      'is_required',
      lambda *_args, **_kwargs: True )

   result = ItineraryCoordinator.set_arrival_time( ARRIVAL_TIME )

   assert result.status == ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP


def Test_SetArrivalTime_TestShortVisitWarning_ExpectTooCloseStatus(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda *_args, **_kwargs: ZOO_HOURS_RECORD )
   monkeypatch.setattr(
      FixedZooScheduleStartTimesBuilder,
      'from_saved_itinerary',
      lambda _saved: [] )
   monkeypatch.setattr(
      ItineraryArrivalTimeValidator,
      'validate_for_zoo_hours',
      lambda *_args, **_kwargs: ItineraryErrorType.SUCCESS )
   monkeypatch.setattr(
      EarlyAdmissionWarningBuilder,
      'is_required',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      ShortVisitWarningBuilder,
      'is_required',
      lambda *_args, **_kwargs: True )

   result = ItineraryCoordinator.set_arrival_time( ARRIVAL_TIME )

   assert result.status == ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE


def Test_SetArrivalTime_TestOverflowWarning_ExpectOutsideHoursStatus(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   overflow_reason = ItineraryResultReason(
      code=ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda *_args, **_kwargs: ZOO_HOURS_RECORD )
   monkeypatch.setattr(
      FixedZooScheduleStartTimesBuilder,
      'from_saved_itinerary',
      lambda _saved: [] )
   monkeypatch.setattr(
      ItineraryArrivalTimeValidator,
      'validate_for_zoo_hours',
      lambda *_args, **_kwargs: ItineraryErrorType.SUCCESS )
   monkeypatch.setattr(
      VisitWindowOverflowIssueFinder,
      'find_from_saved_itinerary',
      lambda *_args, **_kwargs: [ overflow_reason ] )

   result = ItineraryCoordinator.set_arrival_time( ARRIVAL_TIME )

   assert result.status == ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS
   assert result.reasons == [ overflow_reason ]


def Test_SetArrivalTime_TestValidTime_ExpectPersistedAndItinerary(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_times: list[ object ] = []

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda *_args, **_kwargs: ZOO_HOURS_RECORD )
   monkeypatch.setattr(
      FixedZooScheduleStartTimesBuilder,
      'from_saved_itinerary',
      lambda _saved: [] )
   monkeypatch.setattr(
      ItineraryArrivalTimeValidator,
      'validate_for_zoo_hours',
      lambda *_args, **_kwargs: ItineraryErrorType.SUCCESS )
   monkeypatch.setattr(
      EarlyAdmissionWarningBuilder,
      'is_required',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      ShortVisitWarningBuilder,
      'is_required',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      ItineraryTimeProvider,
      'set_itinerary_arrival_time',
      lambda conn, value: saved_times.append( ( conn, value ) ) )
   monkeypatch.setattr(
      ItineraryVisitWindowBuilder,
      'clear_schedules_outside',
      lambda *_args, **_kwargs: None )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda *_args, **_kwargs: ITINERARY )

   result = ItineraryCoordinator.set_arrival_time( ARRIVAL_TIME )

   assert result.success is True
   assert result.itinerary is ITINERARY
   assert saved_times == [ ( STUB_REQUEST_CONNECTION, ARRIVAL_TIME ) ]


def Test_SetDepartureTime_TestClearedTime_ExpectClearsAndReturnsItinerary(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   departure_time = None
   cleared: list[ object ] = []

   monkeypatch.setattr(
      ItineraryTimeProvider,
      'set_itinerary_departure_time',
      lambda conn, value: cleared.append( ( conn, value ) ) )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryVisitWindowBuilder,
      'clear_schedules_outside',
      lambda *_args, **_kwargs: None )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda *_args, **_kwargs: ITINERARY )

   result = ItineraryCoordinator.set_departure_time( departure_time )

   assert result.success is True
   assert result.itinerary is ITINERARY
   assert cleared == [ ( STUB_REQUEST_CONNECTION, departure_time ) ]


def Test_SetDepartureTime_TestValidationFailure_ExpectStatusOnly(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validation_error = ItineraryErrorType.TIME_ORDER_INVALID

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda *_args, **_kwargs: ZOO_HOURS_RECORD )
   monkeypatch.setattr(
      ItineraryDepartureTimeValidator,
      'validate_for_zoo_hours',
      lambda *_args, **_kwargs: validation_error )

   result = ItineraryCoordinator.set_departure_time( DEPARTURE_TIME )

   assert result.status == validation_error
   assert result.itinerary is None


def Test_SetDepartureTime_TestShortVisitWarning_ExpectTooCloseStatus(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda *_args, **_kwargs: ZOO_HOURS_RECORD )
   monkeypatch.setattr(
      ItineraryDepartureTimeValidator,
      'validate_for_zoo_hours',
      lambda *_args, **_kwargs: ItineraryErrorType.SUCCESS )
   monkeypatch.setattr(
      ShortVisitWarningBuilder,
      'is_required',
      lambda *_args, **_kwargs: True )

   result = ItineraryCoordinator.set_departure_time( DEPARTURE_TIME )

   assert result.status == ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE


def Test_SetDepartureTime_TestOverflowWarning_ExpectOutsideHoursStatus(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   overflow_reason = ItineraryResultReason(
      code=ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda *_args, **_kwargs: ZOO_HOURS_RECORD )
   monkeypatch.setattr(
      ItineraryDepartureTimeValidator,
      'validate_for_zoo_hours',
      lambda *_args, **_kwargs: ItineraryErrorType.SUCCESS )
   monkeypatch.setattr(
      VisitWindowOverflowIssueFinder,
      'find_from_saved_itinerary',
      lambda *_args, **_kwargs: [ overflow_reason ] )

   result = ItineraryCoordinator.set_departure_time( DEPARTURE_TIME )

   assert result.status == ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS
   assert result.reasons == [ overflow_reason ]


def Test_SetDepartureTime_TestValidTime_ExpectPersistedAndItinerary(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_times: list[ object ] = []

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: ITINERARY_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda *_args, **_kwargs: ZOO_HOURS_RECORD )
   monkeypatch.setattr(
      ItineraryDepartureTimeValidator,
      'validate_for_zoo_hours',
      lambda *_args, **_kwargs: ItineraryErrorType.SUCCESS )
   monkeypatch.setattr(
      ShortVisitWarningBuilder,
      'is_required',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      ItineraryTimeProvider,
      'set_itinerary_departure_time',
      lambda conn, value: saved_times.append( ( conn, value ) ) )
   monkeypatch.setattr(
      ItineraryVisitWindowBuilder,
      'clear_schedules_outside',
      lambda *_args, **_kwargs: None )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda *_args, **_kwargs: ITINERARY )

   result = ItineraryCoordinator.set_departure_time( DEPARTURE_TIME )

   assert result.success is True
   assert result.itinerary is ITINERARY
   assert saved_times == [ ( STUB_REQUEST_CONNECTION, DEPARTURE_TIME ) ]
