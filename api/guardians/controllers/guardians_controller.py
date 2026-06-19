from __future__ import annotations

from ..coordinators.guardians_coordinator import GuardiansCoordinator
from ...json_handler import JsonRequestHandler


class GuardiansController():
   @staticmethod
   def get_guardians_talks( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      guardians_talks = GuardiansCoordinator.get_guardians_talk_schedule(
         month=data.get( 'month' ),
         day=data.get( 'day' ),
         year=data.get( 'year' ) )

      handler._write_json( {
         'guardians_talks': [ guardians_talk.to_dict() for guardians_talk in guardians_talks ],
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
   def set_guardians_talk_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      monday_time = data.get( 'mondayTime' )
      tuesday_time = data.get( 'tuesdayTime' )
      wednesday_time = data.get( 'wednesdayTime' )
      thursday_time = data.get( 'thursdayTime' )
      friday_time = data.get( 'fridayTime' )
      saturday_time = data.get( 'saturdayTime' )
      sunday_time = data.get( 'sundayTime' )
      message = data.get( 'message' )

      success = GuardiansCoordinator.set_guardians_talk_schedule(
         talk=talk,
         location=location,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         monday_time=monday_time,
         tuesday_time=tuesday_time,
         wednesday_time=wednesday_time,
         thursday_time=thursday_time,
         friday_time=friday_time,
         saturday_time=saturday_time,
         sunday_time=sunday_time,
         message=message )

      response = {
         'success': success,
         'talk': talk,
         'location': location,
         'startDate': schedule_start_date,
         'endDate': schedule_end_date,
         'mondayTime': monday_time,
         'tuesdayTime': tuesday_time,
         'wednesdayTime': wednesday_time,
         'thursdayTime': thursday_time,
         'fridayTime': friday_time,
         'saturdayTime': saturday_time,
         'sundayTime': sunday_time,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set schedule for "{ talk }" at "{ location }".'
         response[ 'errorType' ] = 'overlappingSchedule'

      handler._write_json( response )


   @staticmethod
   def _guardians_talk_schedule_response(
         *,
         success: bool,
         talk: str,
         location: str,
         schedule_start_date: str,
         schedule_end_date: str | None,
         monday_time: str | None,
         tuesday_time: str | None,
         wednesday_time: str | None,
         thursday_time: str | None,
         friday_time: str | None,
         saturday_time: str | None,
         sunday_time: str | None,
         message: str ) -> dict:
      response = {
         'success': success,
         'talk': talk,
         'location': location,
         'startDate': schedule_start_date,
         'endDate': schedule_end_date,
         'mondayTime': monday_time,
         'tuesdayTime': tuesday_time,
         'wednesdayTime': wednesday_time,
         'thursdayTime': thursday_time,
         'fridayTime': friday_time,
         'saturdayTime': saturday_time,
         'sundayTime': sunday_time,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set schedule for "{ talk }" at "{ location }".'

      return response


   @staticmethod
   def replace_guardians_talk_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      monday_time = data.get( 'mondayTime' )
      tuesday_time = data.get( 'tuesdayTime' )
      wednesday_time = data.get( 'wednesdayTime' )
      thursday_time = data.get( 'thursdayTime' )
      friday_time = data.get( 'fridayTime' )
      saturday_time = data.get( 'saturdayTime' )
      sunday_time = data.get( 'sundayTime' )
      message = data.get( 'message' )

      success = GuardiansCoordinator.replace_guardians_talk_schedule_overlaps(
         talk=talk,
         location=location,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         monday_time=monday_time,
         tuesday_time=tuesday_time,
         wednesday_time=wednesday_time,
         thursday_time=thursday_time,
         friday_time=friday_time,
         saturday_time=saturday_time,
         sunday_time=sunday_time,
         message=message )

      handler._write_json(
         GuardiansController._guardians_talk_schedule_response(
            success=success,
            talk=talk,
            location=location,
            schedule_start_date=schedule_start_date,
            schedule_end_date=schedule_end_date,
            monday_time=monday_time,
            tuesday_time=tuesday_time,
            wednesday_time=wednesday_time,
            thursday_time=thursday_time,
            friday_time=friday_time,
            saturday_time=saturday_time,
            sunday_time=sunday_time,
            message=message ) )


   @staticmethod
   def trim_guardians_talk_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      monday_time = data.get( 'mondayTime' )
      tuesday_time = data.get( 'tuesdayTime' )
      wednesday_time = data.get( 'wednesdayTime' )
      thursday_time = data.get( 'thursdayTime' )
      friday_time = data.get( 'fridayTime' )
      saturday_time = data.get( 'saturdayTime' )
      sunday_time = data.get( 'sundayTime' )
      message = data.get( 'message' )

      success = GuardiansCoordinator.trim_guardians_talk_schedule_overlaps(
         talk=talk,
         location=location,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         monday_time=monday_time,
         tuesday_time=tuesday_time,
         wednesday_time=wednesday_time,
         thursday_time=thursday_time,
         friday_time=friday_time,
         saturday_time=saturday_time,
         sunday_time=sunday_time,
         message=message )

      handler._write_json(
         GuardiansController._guardians_talk_schedule_response(
            success=success,
            talk=talk,
            location=location,
            schedule_start_date=schedule_start_date,
            schedule_end_date=schedule_end_date,
            monday_time=monday_time,
            tuesday_time=tuesday_time,
            wednesday_time=wednesday_time,
            thursday_time=thursday_time,
            friday_time=friday_time,
            saturday_time=saturday_time,
            sunday_time=sunday_time,
            message=message ) )


   @staticmethod
   def end_guardians_talk_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      schedule_end_date = data.get( 'endDate' )

      success = GuardiansCoordinator.end_guardians_talk_schedule(
         talk=talk,
         location=location,
         schedule_end_date=schedule_end_date )

      response = {
         'success': success,
         'talk': talk,
         'location': location,
         'endDate': schedule_end_date,
      }

      if not success:
         response[ 'error' ] = f'Could not end schedule for "{ talk }" at "{ location }".'

      handler._write_json( response )


   @staticmethod
   def cancel_guardians_talk_occurrence( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      talk = data.get( 'talk' )
      location = data.get( 'location' )
      date = data.get( 'date' )
      time = data.get( 'time' )

      success = GuardiansCoordinator.cancel_guardians_talk_occurrence(
         talk=talk,
         location=location,
         date=date,
         time=time )

      response = {
         'success': success,
         'talk': talk,
         'location': location,
         'date': date,
         'time': time,
      }

      if not success:
         response[ 'error' ] = (
            f'Could not cancel "{ talk }" at "{ location }" on { date } at { time }.'
         )

      handler._write_json( response )
