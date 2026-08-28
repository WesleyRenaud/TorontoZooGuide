from __future__ import annotations

from ..coordinators.guardians_coordinator import GuardiansCoordinator
from ...json_handler import JsonRequestHandler
from ..scheduling.guardians_talk_map_schedule_collapser import GuardiansTalkMapScheduleCollapser
from ...shared.api_error_response import ApiErrorResponseApplier
from ...shared.enums.api_error_type import ApiErrorType


class GuardiansController():
   @staticmethod
   def get_guardians_talks( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      guardians_talks = GuardiansTalkMapScheduleCollapser.collapse(
         GuardiansCoordinator.get_guardians_talk_schedule(
            month=data.get( 'month' ),
            day=data.get( 'day' ),
            year=data.get( 'year' ) ) )

      handler._write_json( {
         'guardians_talks': guardians_talks,
      } )


   @staticmethod
   def get_guardians_talk_locations( handler: JsonRequestHandler ) -> None:
      guardians_talk_locations = GuardiansCoordinator.get_guardians_talk_locations()

      handler._write_json( {
         'guardians_talk_locations': guardians_talk_locations,
      } )


   @staticmethod
   def get_guardians_talk_names( handler: JsonRequestHandler ) -> None:
      guardians_talks = GuardiansCoordinator.get_guardians_talk_names()

      handler._write_json( {
         'guardians_talks': guardians_talks,
      } )


   @staticmethod
   def get_guardians_talk_names_at_location( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      location = data.get( 'location' )

      guardians_talks = GuardiansCoordinator.get_guardians_talk_names_at_location(
         location=location )

      handler._write_json( {
         'guardians_talks': guardians_talks,
      } )


   @staticmethod
   def get_guardians_talk_occurrences( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )

      occurrences = GuardiansCoordinator.get_guardians_talk_occurrences(
         talk=talk,
         location=location )

      handler._write_json( {
         'occurrences': [ occurrence.to_dict() for occurrence in occurrences ],
         'talk': talk,
         'location': location,
      } )


   @staticmethod
   def _guardians_talk_schedule_response(
         *,
         success: bool,
         talk: str,
         location: str,
         schedule_start_date: str,
         schedule_end_date: str | None,
         schedule_rows: list | None,
         message: str ) -> dict:
      response = {
         'success': success,
         'talk': talk,
         'location': location,
         'startDate': schedule_start_date,
         'endDate': schedule_end_date,
         'scheduleRows': schedule_rows,
         'message': message,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_SET_GUARDIANS_TALK_SCHEDULE, talk=talk, location=location )

      return response


   @staticmethod
   def set_guardians_talk_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      schedule_rows = data.get( 'scheduleRows' )
      message = data.get( 'message' )

      success = GuardiansCoordinator.set_guardians_talk_schedule(
         talk=talk,
         location=location,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         message=message,
         schedule_rows=schedule_rows )

      response = GuardiansController._guardians_talk_schedule_response(
         success=success,
         talk=talk,
         location=location,
         schedule_start_date=schedule_start_date,
         schedule_end_date=schedule_end_date,
         schedule_rows=schedule_rows,
         message=message )

      if not success:
         response[ 'errorType' ] = 'overlappingSchedule'

      handler._write_json( response )


   @staticmethod
   def replace_guardians_talk_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      schedule_rows = data.get( 'scheduleRows' )
      message = data.get( 'message' )

      success = GuardiansCoordinator.replace_guardians_talk_schedule_overlaps(
         talk=talk,
         location=location,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         message=message,
         schedule_rows=schedule_rows )

      handler._write_json(
         GuardiansController._guardians_talk_schedule_response(
            success=success,
            talk=talk,
            location=location,
            schedule_start_date=schedule_start_date,
            schedule_end_date=schedule_end_date,
            schedule_rows=schedule_rows,
            message=message ) )


   @staticmethod
   def trim_guardians_talk_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      schedule_rows = data.get( 'scheduleRows' )
      message = data.get( 'message' )

      success = GuardiansCoordinator.trim_guardians_talk_schedule_overlaps(
         talk=talk,
         location=location,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         message=message,
         schedule_rows=schedule_rows )

      handler._write_json(
         GuardiansController._guardians_talk_schedule_response(
            success=success,
            talk=talk,
            location=location,
            schedule_start_date=schedule_start_date,
            schedule_end_date=schedule_end_date,
            schedule_rows=schedule_rows,
            message=message ) )


   @staticmethod
   def get_guardians_talk_schedule_times( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      schedule_times = GuardiansCoordinator.get_guardians_talk_schedule_times(
         talk=talk,
         location=location )

      handler._write_json( {
         'talk': talk,
         'location': location,
         'times': schedule_times,
      } )


   @staticmethod
   def end_guardians_talk_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      schedule_end_date = data.get( 'endDate' )
      talk_times = data.get( 'times' )

      success = GuardiansCoordinator.end_guardians_talk_schedule(
         talk=talk,
         location=location,
         schedule_end_date=schedule_end_date,
         talk_times=talk_times )

      response = {
         'success': success,
         'talk': talk,
         'location': location,
         'endDate': schedule_end_date,
         'times': talk_times,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_END_GUARDIANS_TALK_SCHEDULE, talk=talk, location=location )

      handler._write_json( response )


   @staticmethod
   def cancel_guardians_talk_occurrence( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      date = data.get( 'date' )
      talk_times = data.get( 'times' )

      success = GuardiansCoordinator.cancel_guardians_talk_occurrence(
         talk=talk,
         location=location,
         date=date,
         talk_times=talk_times )

      response = {
         'success': success,
         'talk': talk,
         'location': location,
         'date': date,
         'times': talk_times,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_CANCEL_GUARDIANS_TALK_OCCURRENCE, talk=talk, location=location, date=date )

      handler._write_json( response )


   @staticmethod
   def add_guardians_talk_occurrence( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      date = data.get( 'date' )
      talk_times = data.get( 'times' )
      success, failure = GuardiansCoordinator.add_guardians_talk_occurrence(
         talk=talk,
         location=location,
         date=date,
         talk_times=talk_times )

      response = {
         'success': success,
         'talk': talk,
         'location': location,
         'date': date,
         'times': talk_times,
      }

      if failure is not None:
         ApiErrorResponseApplier.apply_failure( response, failure )

      handler._write_json( response )
