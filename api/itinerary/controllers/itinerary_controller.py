from __future__ import annotations

from ..coordinators.itinerary_coordinator import ItineraryCoordinator
from ..data_access.itinerary_transportation_input import ItineraryTransportationInput
from ...json_handler import JsonRequestHandler
from ...request_connection import get_connection
from ..results.itinerary_path_builder import ItineraryPathBuilder
from ..results.itinerary_save_result_response_builder import ItinerarySaveResultResponseBuilder
from ..results.itinerary_time_set_result_response_builder import ItineraryTimeSetResultResponseBuilder
from ..results.suppress_itinerary_warning_result_response_builder import SuppressItineraryWarningResultResponseBuilder
from ..scheduling.items.schedule_item_key_mapper import ScheduleItemKeyMapper
from ...shared.api_error_response import apply_api_error
from ...shared.constants import itinerary_config_to_dict
from ...shared.enums.api_error_type import ApiErrorType
from ..wild_encounter_item_key import WildEncounterScheduleItemKey


class ItineraryController():
   @staticmethod
   def set_itinerary( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      date = data.get( 'date' )
      arrival_time = data.get( 'arrivalTime' )
      departure_time = data.get( 'departureTime' )
      selected_exhibits = data.get( 'selectedExhibits' )
      animals = data.get( 'animals' )
      attractions = data.get( 'attractions' )
      transportations = ItineraryTransportationInput.from_wires(
         data.get( 'transportations' ) )
      guardians_talks = data.get( 'guardiansTalks' )
      wild_encounters = WildEncounterScheduleItemKey.from_wires(
         data.get( 'wildEncounters' ) )
      temp = data.get( 'temp' )
      overriding_conflicting_guardians_talks = bool(
         data.get( 'overridingConflictingGuardiansTalks' ) )
      confirming_short_visit = bool( data.get( 'confirmingShortVisit' ) )
      confirming_early_admission = bool(
         data.get( 'confirmingEarlyAdmission' ) )
      confirming_guardians_talk_unschedule = bool(
         data.get( 'confirmingGuardiansTalkUnschedule' ) )
      confirming_wild_encounter_unschedule = bool(
         data.get( 'confirmingWildEncounterUnschedule' ) )
      confirming_fixed_time_item_long_wait = bool(
         data.get( 'confirmingFixedTimeItemLongWait' ) )
      confirming_guardians_talk_without_animal = bool(
         data.get( 'confirmingGuardiansTalkWithoutAnimal' ) )
      confirming_attraction_without_animal = bool(
         data.get( 'confirmingAttractionWithoutAnimal' ) )

      save_result = ItineraryCoordinator.set_itinerary(
         date=date,
         arrival_time=arrival_time,
         departure_time=departure_time,
         selected_exhibits=selected_exhibits,
         animals=animals,
         attractions=attractions,
         transportations=transportations,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters,
         visit_date_temp=temp,
         overriding_conflicting_guardians_talks=(
            overriding_conflicting_guardians_talks ),
         confirming_short_visit=confirming_short_visit,
         confirming_early_admission=confirming_early_admission,
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ),
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ),
         confirming_fixed_time_item_long_wait=(
            confirming_fixed_time_item_long_wait ),
         confirming_guardians_talk_without_animal=(
            confirming_guardians_talk_without_animal ),
         confirming_attraction_without_animal=(
            confirming_attraction_without_animal ) )

      response = ItinerarySaveResultResponseBuilder.to_dict(
         save_result,
         conn=get_connection(),
         include_config=True )

      handler._write_json( response )


   @staticmethod
   def get_itinerary_date( handler: JsonRequestHandler ) -> None:
      date = ItineraryCoordinator.get_itinerary_date()

      handler._write_json( { 'date': date } )


   @staticmethod
   def schedule_itinerary_item( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      schedule_item_key = ScheduleItemKeyMapper.from_wire(
         data.get( 'itemType' ),
         data.get( 'key' ) )
      start_time = data.get( 'startTime' )
      duration_minutes = data.get( 'durationMinutes' )
      confirming_schedule_item_not_on_itinerary = bool(
         data.get( 'confirmingScheduleItemNotOnItinerary' ) )
      confirming_attraction_outside_operating_hours = bool(
         data.get( 'confirmingAttractionOutsideOperatingHours' ) )
      confirming_guardians_talk_unschedule = bool(
         data.get( 'confirmingGuardiansTalkUnschedule' ) )
      confirming_wild_encounter_unschedule = bool(
         data.get( 'confirmingWildEncounterUnschedule' ) )
      confirming_fixed_time_item_long_wait = bool(
         data.get( 'confirmingFixedTimeItemLongWait' ) )
      confirming_guardians_talk_without_animal = bool(
         data.get( 'confirmingGuardiansTalkWithoutAnimal' ) )

      save_result = ItineraryCoordinator.schedule_itinerary_item(
         schedule_item_key,
         start_time=start_time,
         duration_minutes=duration_minutes,
         confirming_schedule_item_not_on_itinerary=(
            confirming_schedule_item_not_on_itinerary
         ),
         confirming_attraction_outside_operating_hours=(
            confirming_attraction_outside_operating_hours
         ),
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ),
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ),
         confirming_fixed_time_item_long_wait=(
            confirming_fixed_time_item_long_wait ),
         confirming_guardians_talk_without_animal=(
            confirming_guardians_talk_without_animal ) )

      response = ItinerarySaveResultResponseBuilder.to_dict(
         save_result,
         conn=get_connection(),
         include_config=True )

      handler._write_json( response )


   @staticmethod
   def bulk_schedule_itinerary( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      temp = data.get( 'temp' )
      confirming_fixed_time_item_long_wait = bool(
         data.get( 'confirmingFixedTimeItemLongWait' ) )

      save_result = ItineraryCoordinator.bulk_schedule_itinerary(
         visit_date_temp=temp,
         confirming_fixed_time_item_long_wait=(
            confirming_fixed_time_item_long_wait ),
 )

      response = ItinerarySaveResultResponseBuilder.to_dict(
         save_result,
         conn=get_connection(),
         include_config=True )

      handler._write_json( response )


   @staticmethod
   def unschedule_all_itinerary_items( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      temp = data.get( 'temp' )

      save_result = ItineraryCoordinator.unschedule_all_itinerary_items(
         visit_date_temp=temp )

      response = ItinerarySaveResultResponseBuilder.to_dict(
         save_result,
         conn=get_connection(),
         include_config=True )

      handler._write_json( response )


   @staticmethod
   def unschedule_itinerary_item( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      schedule_item_key = ScheduleItemKeyMapper.from_wire(
         data.get( 'itemType' ),
         data.get( 'key' ) )

      save_result = ItineraryCoordinator.unschedule_itinerary_item(
         schedule_item_key )

      response = ItinerarySaveResultResponseBuilder.to_dict(
         save_result,
         conn=get_connection() )

      handler._write_json( response )


   @staticmethod
   def remove_item_from_itinerary( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      schedule_item_key = ScheduleItemKeyMapper.from_wire(
         data.get( 'itemType' ),
         data.get( 'key' ) )

      save_result = ItineraryCoordinator.remove_itinerary_item(
         schedule_item_key )

      response = ItinerarySaveResultResponseBuilder.to_dict(
         save_result,
         conn=get_connection() )

      handler._write_json( response )


   @staticmethod
   def set_itinerary_arrival_time( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      arrival_time = data.get( 'arrivalTime' )
      confirming_short_visit = bool( data.get( 'confirmingShortVisit' ) )
      confirming_early_admission = bool(
         data.get( 'confirmingEarlyAdmission' ) )

      save_result = ItineraryCoordinator.set_arrival_time(
         arrival_time=arrival_time,
         confirming_short_visit=confirming_short_visit,
         confirming_early_admission=confirming_early_admission )

      response = ItineraryTimeSetResultResponseBuilder.to_dict(
         save_result,
         conn=get_connection() )

      handler._write_json( response )


   @staticmethod
   def set_itinerary_departure_time( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      departure_time = data.get( 'departureTime' )
      confirming_short_visit = bool( data.get( 'confirmingShortVisit' ) )

      save_result = ItineraryCoordinator.set_departure_time(
         departure_time=departure_time,
         confirming_short_visit=confirming_short_visit )

      response = ItineraryTimeSetResultResponseBuilder.to_dict(
         save_result,
         conn=get_connection() )

      handler._write_json( response )


   @staticmethod
   def suppress_itinerary_warning( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      warning_type = data.get( 'warningType' )

      result = ItineraryCoordinator.suppress_itinerary_warning(
         warning_type=warning_type )

      response = SuppressItineraryWarningResultResponseBuilder.to_dict(
         result,
         conn=get_connection() )

      handler._write_json( response )


   @staticmethod
   def get_itinerary( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      temp = data.get( 'temp' )

      itinerary = ItineraryCoordinator.get_itinerary( visit_date_temp=temp )

      conn = get_connection()
      handler._write_json( {
         'itinerary': itinerary.to_dict(),
         'itinerary_config': itinerary_config_to_dict( conn ),
         'itinerary_path': ItineraryPathBuilder.build( conn ),
      } )


   @staticmethod
   def clear_itinerary( handler: JsonRequestHandler ) -> None:
      success = ItineraryCoordinator.clear_itinerary()

      response = {
         'success': success
      }

      if not success:
         apply_api_error( response, ApiErrorType.COULD_NOT_CLEAR_ITINERARY )

      handler._write_json( response )


   @staticmethod
   def accept_itinerary( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      temp = data.get( 'temp' )
      animals_to_keep = data.get( 'animalsToKeep' )
      attractions_to_keep = data.get( 'attractionsToKeep' )

      success = ItineraryCoordinator.accept_itinerary(
         animals_to_keep=animals_to_keep,
         attractions_to_keep=attractions_to_keep )
      itinerary = (
         ItineraryCoordinator.get_itinerary( visit_date_temp=temp )
         if success
         else None
      )

      conn = get_connection()
      response = {
         'success': success,
         'itinerary': itinerary.to_dict() if itinerary != None else None,
         'itinerary_config': itinerary_config_to_dict( conn ),
         'itinerary_path': ItineraryPathBuilder.build( conn ),
      }

      if not success:
         apply_api_error( response, ApiErrorType.COULD_NOT_ACCEPT_ITINERARY_CHANGES )

      handler._write_json( response )
