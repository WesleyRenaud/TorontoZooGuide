from __future__ import annotations

from ..coordinators.itinerary_coordinator import ItineraryCoordinator
from ...json_handler import JsonRequestHandler
from ...request_connection import get_connection
from ..results.itinerary_result_response import itinerary_result_to_dict
from ..results.itinerary_result_response import itinerary_time_set_result_to_dict
from ..results.itinerary_result_response import suppress_itinerary_warning_result_to_dict
from ..scheduling.items.map_schedule_item_key_from_wire import map_schedule_item_key_from_wire
from ...shared.constants import itinerary_config_to_dict
from ..wild_encounter_item_key import WildEncounterScheduleItemKey


class ItineraryController():
   @staticmethod
   def set_itinerary( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      date = data.get( 'date' )
      arrival_time = data.get( 'arrivalTime' )
      departure_time = data.get( 'departureTime' )
      animals = data.get( 'animals' )
      attractions = data.get( 'attractions' )
      guardians_talks = data.get( 'guardiansTalks' )
      wild_encounters = WildEncounterScheduleItemKey.from_wires(
         data.get( 'wildEncounters' ) )
      selected_exhibits = data.get( 'selectedExhibits' )
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

      save_result = ItineraryCoordinator.set_itinerary(
         date=date,
         arrival_time=arrival_time,
         departure_time=departure_time,
         animals=animals,
         attractions=attractions,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters,
         selected_exhibits=selected_exhibits,
         visit_date_temp=temp,
         overriding_conflicting_guardians_talks=(
            overriding_conflicting_guardians_talks ),
         confirming_short_visit=confirming_short_visit,
         confirming_early_admission=confirming_early_admission,
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ),
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ) )

      response = itinerary_result_to_dict(
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

      schedule_item_key = map_schedule_item_key_from_wire(
         data.get( 'itemType' ),
         data.get( 'key' ) )
      start_time = data.get( 'startTime' )
      duration_minutes = data.get( 'durationMinutes' )
      confirming_schedule_item_not_on_itinerary = bool(
         data.get( 'confirmingScheduleItemNotOnItinerary' ) )
      confirming_guardians_talk_unschedule = bool(
         data.get( 'confirmingGuardiansTalkUnschedule' ) )
      confirming_wild_encounter_unschedule = bool(
         data.get( 'confirmingWildEncounterUnschedule' ) )

      save_result = ItineraryCoordinator.schedule_itinerary_item(
         schedule_item_key,
         start_time=start_time,
         duration_minutes=duration_minutes,
         confirming_schedule_item_not_on_itinerary=(
            confirming_schedule_item_not_on_itinerary
         ),
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ),
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ) )

      response = itinerary_result_to_dict(
         save_result,
         conn=get_connection(),
         include_config=True )

      handler._write_json( response )


   @staticmethod
   def bulk_schedule_animals( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      temp = data.get( 'temp' )

      save_result = ItineraryCoordinator.bulk_schedule_animals(
         visit_date_temp=temp )

      response = itinerary_result_to_dict(
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

      response = itinerary_result_to_dict(
         save_result,
         conn=get_connection(),
         include_config=True )

      handler._write_json( response )


   @staticmethod
   def unschedule_itinerary_item( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      schedule_item_key = map_schedule_item_key_from_wire(
         data.get( 'itemType' ),
         data.get( 'key' ) )

      save_result = ItineraryCoordinator.unschedule_itinerary_item(
         schedule_item_key )

      response = itinerary_result_to_dict(
         save_result,
         conn=get_connection() )

      handler._write_json( response )


   @staticmethod
   def remove_item_from_itinerary( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      schedule_item_key = map_schedule_item_key_from_wire(
         data.get( 'itemType' ),
         data.get( 'key' ) )

      save_result = ItineraryCoordinator.remove_itinerary_item(
         schedule_item_key )

      response = itinerary_result_to_dict(
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

      response = itinerary_time_set_result_to_dict(
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

      response = itinerary_time_set_result_to_dict(
         save_result,
         conn=get_connection() )

      handler._write_json( response )


   @staticmethod
   def suppress_itinerary_warning( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      warning_type = data.get( 'warningType' )

      result = ItineraryCoordinator.suppress_itinerary_warning(
         warning_type=warning_type )

      response = suppress_itinerary_warning_result_to_dict(
         result,
         conn=get_connection() )

      handler._write_json( response )


   @staticmethod
   def get_itinerary( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      temp = data.get( 'temp' )

      itinerary = ItineraryCoordinator.get_itinerary( visit_date_temp=temp )

      handler._write_json( {
         'itinerary': itinerary.to_dict(),
         'itinerary_config': itinerary_config_to_dict( get_connection() ),
      } )


   @staticmethod
   def clear_itinerary( handler: JsonRequestHandler ) -> None:
      success = ItineraryCoordinator.clear_itinerary()

      response = {
         'success': success
      }

      if not success:
         response[ 'error' ] = 'Could not clear itinerary.'

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

      response = {
         'success': success,
         'itinerary': itinerary.to_dict() if itinerary != None else None,
         'itinerary_config': itinerary_config_to_dict( get_connection() ),
      }

      if not success:
         response[ 'error' ] = 'Could not accept itinerary changes.'

      handler._write_json( response )
