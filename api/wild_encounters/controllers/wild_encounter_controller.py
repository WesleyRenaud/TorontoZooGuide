from __future__ import annotations

from ..coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ...json_handler import JsonRequestHandler
from ..scheduling.collapse_wild_encounters_for_map_builder import CollapseWildEncountersForMapBuilder
from ...shared.api_error_response import apply_api_error
from ...shared.enums.api_error_type import ApiErrorType


class WildEncounterController():
   @staticmethod
   def get_wild_encounters( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounters = CollapseWildEncountersForMapBuilder.build(
         WildEncounterCoordinator.get_available_wild_encounters(
            month=data.get( 'month' ),
            day=data.get( 'day' ),
            year=data.get( 'year' ) ) )

      handler._write_json( {
         'wild_encounters': wild_encounters,
      } )


   @staticmethod
   def get_wild_encounter_names( handler: JsonRequestHandler ) -> None:
      wild_encounters = WildEncounterCoordinator.get_wild_encounter_names()

      handler._write_json( {
         'wild_encounters': wild_encounters,
      } )


   @staticmethod
   def get_wild_encounter_occurrences( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )

      occurrences = WildEncounterCoordinator.get_wild_encounter_occurrences(
         wild_encounter_name=wild_encounter )

      handler._write_json( {
         'occurrences': [ occurrence.to_dict() for occurrence in occurrences ],
         'wildEncounter': wild_encounter,
      } )


   @staticmethod
   def _wild_encounter_schedule_response(
         *,
         success: bool,
         wild_encounter: str,
         schedule_start_date: str,
         schedule_end_date: str | None,
         schedule_rows: list | None,
         message: str ) -> dict:
      response = {
         'success': success,
         'wildEncounter': wild_encounter,
         'startDate': schedule_start_date,
         'endDate': schedule_end_date,
         'scheduleRows': schedule_rows,
         'message': message,
      }

      if not success:
         apply_api_error( response, ApiErrorType.COULD_NOT_SET_WILD_ENCOUNTER_SCHEDULE, name=wild_encounter )

      return response


   @staticmethod
   def set_wild_encounter_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      schedule_rows = data.get( 'scheduleRows' )
      message = data.get( 'message' )

      success = WildEncounterCoordinator.set_wild_encounter_schedule(
         wild_encounter_name=wild_encounter,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         message=message,
         schedule_rows=schedule_rows )

      response = WildEncounterController._wild_encounter_schedule_response(
         success=success,
         wild_encounter=wild_encounter,
         schedule_start_date=schedule_start_date,
         schedule_end_date=schedule_end_date,
         schedule_rows=schedule_rows,
         message=message )

      if not success:
         response[ 'errorType' ] = 'overlappingSchedule'

      handler._write_json( response )


   @staticmethod
   def replace_wild_encounter_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      schedule_rows = data.get( 'scheduleRows' )
      message = data.get( 'message' )

      success = WildEncounterCoordinator.replace_wild_encounter_schedule_overlaps(
         wild_encounter_name=wild_encounter,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         message=message,
         schedule_rows=schedule_rows )

      handler._write_json(
         WildEncounterController._wild_encounter_schedule_response(
            success=success,
            wild_encounter=wild_encounter,
            schedule_start_date=schedule_start_date,
            schedule_end_date=schedule_end_date,
            schedule_rows=schedule_rows,
            message=message ) )


   @staticmethod
   def trim_wild_encounter_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      schedule_rows = data.get( 'scheduleRows' )
      message = data.get( 'message' )

      success = WildEncounterCoordinator.trim_wild_encounter_schedule_overlaps(
         wild_encounter_name=wild_encounter,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         message=message,
         schedule_rows=schedule_rows )

      handler._write_json(
         WildEncounterController._wild_encounter_schedule_response(
            success=success,
            wild_encounter=wild_encounter,
            schedule_start_date=schedule_start_date,
            schedule_end_date=schedule_end_date,
            schedule_rows=schedule_rows,
            message=message ) )


   @staticmethod
   def get_wild_encounter_schedule_times( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      schedule_times = WildEncounterCoordinator.get_wild_encounter_schedule_times(
         wild_encounter_name=wild_encounter )

      handler._write_json( {
         'wildEncounter': wild_encounter,
         'times': schedule_times,
      } )


   @staticmethod
   def end_wild_encounter_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      schedule_end_date = data.get( 'endDate' )
      encounter_times = data.get( 'times' )

      success = WildEncounterCoordinator.end_wild_encounter_schedule(
         wild_encounter_name=wild_encounter,
         schedule_end_date=schedule_end_date,
         encounter_times=encounter_times )

      response = {
         'success': success,
         'wildEncounter': wild_encounter,
         'endDate': schedule_end_date,
         'times': encounter_times,
      }

      if not success:
         apply_api_error( response, ApiErrorType.COULD_NOT_END_WILD_ENCOUNTER_SCHEDULE, name=wild_encounter )

      handler._write_json( response )


   @staticmethod
   def cancel_wild_encounter_occurrence( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      date = data.get( 'date' )
      encounter_times = data.get( 'times' )

      success = WildEncounterCoordinator.cancel_wild_encounter_occurrence(
         wild_encounter_name=wild_encounter,
         date=date,
         encounter_times=encounter_times )

      response = {
         'success': success,
         'wildEncounter': wild_encounter,
         'date': date,
         'times': encounter_times,
      }

      if not success:
         apply_api_error( response, ApiErrorType.COULD_NOT_CANCEL_WILD_ENCOUNTER_OCCURRENCE, name=wild_encounter, date=date )

      handler._write_json( response )
