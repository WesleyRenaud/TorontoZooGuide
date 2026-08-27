from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.accept_itinerary_provider import AcceptItineraryProvider
from ..data_access.clear_itinerary_provider import ClearItineraryProvider
from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_save_input_mapper import ItinerarySaveInputMapper
from ..data_access.itinerary_time_provider import ItineraryTimeProvider
from ..data_access.itinerary_transportation_input import ItineraryTransportationInput
from ..domain.itinerary_builder import ItineraryBuilder
from ..domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...models import Itinerary
from ..operations import remove_itinerary_item as remove_itinerary_item_logic
from ..operations import set_itinerary as set_itinerary_logic
from ..operations import suppress_itinerary_warning as suppress_itinerary_warning_logic
from ..operations import unschedule_all_itinerary_items as unschedule_all_itinerary_items_logic
from ..operations import unschedule_itinerary_item as unschedule_itinerary_item_logic
from ..operations.suppress_itinerary_warning import SuppressItineraryWarningResult
from ...request_connection import get_connection
from ..results.itinerary_save_result import ItinerarySaveResult
from ..results.itinerary_time_set_result import ItineraryTimeSetResult
from ..scheduling.bulk.bulk_schedule_itinerary_runner import BulkScheduleItineraryRunner
from ..scheduling.bulk.bulk_schedule_stop_selector import BulkScheduleStopSelector
from ..scheduling.items import schedule_itinerary_item as schedule_itinerary_item_logic
from ..scheduling.items.schedule_item_key import ScheduleItemKey
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryErrorType
from ...types import Connection, DateInput, DurationInput, TimeInput
from ..validation.fixed_zoo_schedule_start_times_builder import FixedZooScheduleStartTimesBuilder
from ..validation.itinerary_arrival_time_validator import ItineraryArrivalTimeValidator
from ..validation.itinerary_departure_time_validator import ItineraryDepartureTimeValidator
from ..warnings.early_admission_warning_builder import EarlyAdmissionWarningBuilder
from ..warnings.short_visit_warning_builder import ShortVisitWarningBuilder
from ..wild_encounter_item_key import WildEncounterScheduleItemKey
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ...zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider


class ItineraryCoordinator():
   @classmethod
   def _current_itinerary( cls, conn: Connection ) -> Itinerary:
      return ItineraryBuilder.build_current(
         ItineraryProvider.fetch_saved_itinerary( conn ),
         animal_coordinator=AnimalCoordinator,
         attraction_coordinator=AttractionCoordinator,
         guardians_coordinator=GuardiansCoordinator,
         wild_encounter_coordinator=WildEncounterCoordinator )


   @classmethod
   def _time_set_result(
         cls,
         conn: Connection,
         suppressed_warnings: list[ ItineraryErrorType ] | None = None ) -> ItineraryTimeSetResult:
      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )

      ItineraryVisitWindowBuilder.clear_schedules_outside(
         conn,
         arrival_time=saved_itinerary.arrival_time,
         departure_time=saved_itinerary.departure_time )

      return ItineraryTimeSetResult(
         suppressed_warnings=suppressed_warnings or [],
         itinerary=cls._current_itinerary( conn ) )


   @classmethod
   def get_itinerary_date( cls ) -> str | None:
      return ItineraryProvider.fetch_itinerary_date( get_connection() )


   @classmethod
   def get_itinerary( cls, visit_date_temp: float | None = None ) -> Itinerary:
      return ItineraryBuilder.build_current(
         saved_itinerary=ItineraryProvider.fetch_saved_itinerary( get_connection() ),
         animal_coordinator=AnimalCoordinator,
         attraction_coordinator=AttractionCoordinator,
         guardians_coordinator=GuardiansCoordinator,
         wild_encounter_coordinator=WildEncounterCoordinator,
         visit_date_temp=visit_date_temp )


   @classmethod
   def set_itinerary(
         cls,
         date: DateInput,
         selected_exhibits: list[ str ] | None = None,
         animals: list[ dict[ str, str ] ] | None = None,
         attractions: list[ str ] | None = None,
         guardians_talks: list[ dict[ str, str | None ] ] | None = None,
         wild_encounters: list[ WildEncounterScheduleItemKey ] | None = None,
         transportations: list[ ItineraryTransportationInput ] | None = None,
         arrival_time: TimeInput = None,
         departure_time: TimeInput = None,
         visit_date_temp: float | None = None,
         overriding_conflicting_guardians_talks: bool = False,
         confirming_short_visit: bool = False,
         confirming_early_admission: bool = False,
         confirming_guardians_talk_unschedule: bool = False,
         confirming_wild_encounter_unschedule: bool = False,
         confirming_fixed_time_item_long_wait: bool = False,
         confirming_guardians_talk_without_animal: bool = False,
         confirming_attraction_without_animal: bool = False ) -> ItinerarySaveResult:
      return set_itinerary_logic.set_itinerary(
         get_connection(),
         date=date,
         arrival_time=arrival_time,
         departure_time=departure_time,
         selected_exhibits=selected_exhibits,
         animals=animals,
         attractions=attractions,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters,
         transportations=transportations,
         visit_date_temp=visit_date_temp,
         overriding_conflicting_guardians_talks=(
            overriding_conflicting_guardians_talks ),
         confirming_short_visit=confirming_short_visit,
         confirming_early_admission=confirming_early_admission,
         confirming_guardians_talk_unschedule=confirming_guardians_talk_unschedule,
         confirming_wild_encounter_unschedule=confirming_wild_encounter_unschedule,
         confirming_fixed_time_item_long_wait=(
            confirming_fixed_time_item_long_wait ),
         confirming_guardians_talk_without_animal=(
            confirming_guardians_talk_without_animal ),
         confirming_attraction_without_animal=(
            confirming_attraction_without_animal ),
         animal_coordinator=AnimalCoordinator,
         attraction_coordinator=AttractionCoordinator,
         guardians_coordinator=GuardiansCoordinator,
         wild_encounter_coordinator=WildEncounterCoordinator )


   @classmethod
   def schedule_itinerary_item(
         cls,
         schedule_item_key: ScheduleItemKey | None,
         *,
         start_time: TimeInput = None,
         duration_minutes: DurationInput = None,
         confirming_schedule_item_not_on_itinerary: bool = False,
         confirming_attraction_outside_operating_hours: bool = False,
         confirming_guardians_talk_unschedule: bool = False,
         confirming_wild_encounter_unschedule: bool = False,
         confirming_fixed_time_item_long_wait: bool = False,
         confirming_guardians_talk_without_animal: bool = False ) -> ItinerarySaveResult:
      return schedule_itinerary_item_logic.schedule_itinerary_item(
         get_connection(),
         schedule_item_key,
         start_time=start_time,
         duration_minutes=duration_minutes,
         animal_coordinator=AnimalCoordinator,
         attraction_coordinator=AttractionCoordinator,
         guardians_coordinator=GuardiansCoordinator,
         wild_encounter_coordinator=WildEncounterCoordinator,
         confirming_schedule_item_not_on_itinerary=(
            confirming_schedule_item_not_on_itinerary
         ),
         confirming_attraction_outside_operating_hours=(
            confirming_attraction_outside_operating_hours
         ),
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule
         ),
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule
         ),
         confirming_fixed_time_item_long_wait=(
            confirming_fixed_time_item_long_wait
         ),
         confirming_guardians_talk_without_animal=(
            confirming_guardians_talk_without_animal
         ) )


   @classmethod
   def bulk_schedule_itinerary(
         cls,
         visit_date_temp: float | None = None,
         *,
         confirming_fixed_time_item_long_wait: bool = False ) -> ItinerarySaveResult:
      conn = get_connection()
      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )

      return BulkScheduleItineraryRunner.run(
         conn,
         animal_coordinator=AnimalCoordinator,
         attraction_coordinator=AttractionCoordinator,
         guardians_coordinator=GuardiansCoordinator,
         wild_encounter_coordinator=WildEncounterCoordinator,
         visit_date_temp=visit_date_temp,
         confirming_fixed_time_item_long_wait=(
            confirming_fixed_time_item_long_wait ),
         stops_to_schedule=BulkScheduleStopSelector.stops(
            saved_itinerary,
            only_previously_scheduled=False ) )


   @classmethod
   def clear_itinerary( cls ) -> bool:
      return ClearItineraryProvider.clear_itinerary( get_connection() )


   @classmethod
   def unschedule_all_itinerary_items(
         cls,
         visit_date_temp: float | None = None ) -> ItinerarySaveResult:
      return unschedule_all_itinerary_items_logic.unschedule_all_itinerary_items(
         get_connection(),
         animal_coordinator=AnimalCoordinator,
         attraction_coordinator=AttractionCoordinator,
         guardians_coordinator=GuardiansCoordinator,
         wild_encounter_coordinator=WildEncounterCoordinator,
         visit_date_temp=visit_date_temp )


   @classmethod
   def unschedule_itinerary_item(
         cls,
         schedule_item_key: ScheduleItemKey | None ) -> ItinerarySaveResult:
      return unschedule_itinerary_item_logic.unschedule_itinerary_item(
         get_connection(),
         schedule_item_key )


   @classmethod
   def remove_itinerary_item(
         cls,
         schedule_item_key: ScheduleItemKey | None ) -> ItinerarySaveResult:
      return remove_itinerary_item_logic.remove_itinerary_item(
         get_connection(),
         schedule_item_key )


   @classmethod
   def suppress_itinerary_warning(
         cls,
         warning_type: str ) -> SuppressItineraryWarningResult:
      return suppress_itinerary_warning_logic.suppress_itinerary_warning(
         get_connection(),
         warning_type )


   @classmethod
   def set_arrival_time(
         cls,
         arrival_time: TimeInput,
         *,
         confirming_short_visit: bool = False,
         confirming_early_admission: bool = False ) -> ItineraryTimeSetResult:
      conn = get_connection()
      normalized_arrival_time = DateValues.normalize_itinerary_schedule_time(
         arrival_time )

      if normalized_arrival_time is None:
         ItineraryTimeProvider.set_itinerary_arrival_time( conn, None )
         return cls._time_set_result( conn )

      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
      zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record(
         conn,
         ItineraryProvider.fetch_itinerary_date( conn ) )

      validation_error = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
         normalized_arrival_time,
         zoo_hours_record,
         departure_time=saved_itinerary.departure_time,
         fixed_zoo_start_times=(
            FixedZooScheduleStartTimesBuilder.from_saved_itinerary(
               saved_itinerary ) ) )

      if validation_error != ItineraryErrorType.SUCCESS:
         return ItineraryTimeSetResult( status=validation_error )

      suppressed_warnings: list[ ItineraryErrorType ] = []

      if EarlyAdmissionWarningBuilder.is_required(
            conn,
            normalized_arrival_time,
            zoo_hours_record,
            confirming_early_admission=confirming_early_admission,
            suppressed_warnings=suppressed_warnings ):
         return ItineraryTimeSetResult(
            status=ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
            suppressed_warnings=suppressed_warnings )

      if ShortVisitWarningBuilder.is_required(
            conn,
            normalized_arrival_time,
            saved_itinerary.departure_time,
            confirming_short_visit=confirming_short_visit,
            suppressed_warnings=suppressed_warnings ):
         return ItineraryTimeSetResult(
            status=ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
            suppressed_warnings=suppressed_warnings )

      ItineraryTimeProvider.set_itinerary_arrival_time( conn, normalized_arrival_time )

      return cls._time_set_result(
         conn,
         suppressed_warnings=suppressed_warnings )


   @classmethod
   def set_departure_time(
         cls,
         departure_time: TimeInput,
         *,
         confirming_short_visit: bool = False ) -> ItineraryTimeSetResult:
      conn = get_connection()
      normalized_departure_time = DateValues.normalize_itinerary_schedule_time(
         departure_time )

      if normalized_departure_time is None:
         ItineraryTimeProvider.set_itinerary_departure_time( conn, None )
         return cls._time_set_result( conn )

      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
      zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record(
         conn,
         ItineraryProvider.fetch_itinerary_date( conn ) )

      validation_error = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
         normalized_departure_time,
         zoo_hours_record,
         arrival_time=saved_itinerary.arrival_time )

      if validation_error != ItineraryErrorType.SUCCESS:
         return ItineraryTimeSetResult( status=validation_error )

      suppressed_warnings: list[ ItineraryErrorType ] = []

      if ShortVisitWarningBuilder.is_required(
            conn,
            saved_itinerary.arrival_time,
            normalized_departure_time,
            confirming_short_visit=confirming_short_visit,
            suppressed_warnings=suppressed_warnings ):
         return ItineraryTimeSetResult(
            status=ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
            suppressed_warnings=suppressed_warnings )

      ItineraryTimeProvider.set_itinerary_departure_time( conn, normalized_departure_time )

      return cls._time_set_result(
         conn,
         suppressed_warnings=suppressed_warnings )


   @classmethod
   def accept_itinerary(
         cls,
         animals_to_keep: list[ dict[ str, str ] ] | None = None,
         attractions_to_keep: list[ str ] | None = None ) -> bool:
      return AcceptItineraryProvider.accept_itinerary(
         get_connection(),
         animals_to_keep=ItinerarySaveInputMapper.map_animal_inputs( animals_to_keep ),
         attractions_to_keep=ItinerarySaveInputMapper.map_named_strings( attractions_to_keep ) )
