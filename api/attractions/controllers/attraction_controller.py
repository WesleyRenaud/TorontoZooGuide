from __future__ import annotations

from ..coordinators.attraction_coordinator import AttractionCoordinator
from ...json_handler import JsonRequestHandler
from ...shared.calendar_dates import DateValues


class AttractionController():
   @staticmethod
   def get_attractions( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      attractions = AttractionCoordinator.get_attractions(
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ),
         include_closed_attractions=data.get( 'includeClosedAttractions' ) or False )

      handler._write_json( {
         'attractions': [ attraction.to_dict() for attraction in attractions ],
      } )


   @staticmethod
   def get_attraction_names( handler: JsonRequestHandler ) -> None:
      attractions = AttractionCoordinator.get_attraction_names()

      handler._write_json( {
         'attractions': attractions,
      } )


   @staticmethod
   def set_attraction_closed( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      attraction = data.get( 'attraction' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = AttractionCoordinator.set_attraction_as_closed(
         attraction=attraction,
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'attraction': attraction,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set "{ attraction }" as closed.'

      handler._write_json( response )


   @staticmethod
   def set_attraction_closure_override( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      attraction = data.get( 'attraction' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = AttractionCoordinator.set_attraction_closure_override(
         attraction=attraction,
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'attraction': attraction,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not create closure override for "{ attraction }".'

      handler._write_json( response )


   @staticmethod
   def set_attraction_opening_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      attraction = data.get( 'attraction' )
      schedule_start_date = data.get( 'scheduleStartDate' )
      schedule_end_date = data.get( 'scheduleEndDate' )
      monday = data.get( 'monday' )
      tuesday = data.get( 'tuesday' )
      wednesday = data.get( 'wednesday' )
      thursday = data.get( 'thursday' )
      friday = data.get( 'friday' )
      saturday = data.get( 'saturday' )
      sunday = data.get( 'sunday' )
      holidays_only = data.get( 'holidaysOnly' )
      message = data.get( 'message' )

      success = AttractionCoordinator.set_attraction_opening_schedule(
         attraction=attraction,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )

      response = {
         'success': success,
         'attraction': attraction,
         'scheduleStartDate': schedule_start_date,
         'scheduleEndDate': schedule_end_date,
         'monday': monday,
         'tuesday': tuesday,
         'wednesday': wednesday,
         'thursday': thursday,
         'friday': friday,
         'saturday': saturday,
         'sunday': sunday,
         'holidaysOnly': holidays_only,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set opening schedule for "{ attraction }".'
         response[ 'errorType' ] = 'overlappingSchedule'

      handler._write_json( response )


   @staticmethod
   def replace_attraction_opening_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      attraction = data.get( 'attraction' )
      schedule_start_date = data.get( 'scheduleStartDate' )
      schedule_end_date = data.get( 'scheduleEndDate' )
      monday = data.get( 'monday' )
      tuesday = data.get( 'tuesday' )
      wednesday = data.get( 'wednesday' )
      thursday = data.get( 'thursday' )
      friday = data.get( 'friday' )
      saturday = data.get( 'saturday' )
      sunday = data.get( 'sunday' )
      holidays_only = data.get( 'holidaysOnly' )
      message = data.get( 'message' )

      success = AttractionCoordinator.replace_attraction_opening_schedule_overlaps(
         attraction=attraction,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )

      response = {
         'success': success,
         'attraction': attraction,
         'scheduleStartDate': schedule_start_date,
         'scheduleEndDate': schedule_end_date,
         'monday': monday,
         'tuesday': tuesday,
         'wednesday': wednesday,
         'thursday': thursday,
         'friday': friday,
         'saturday': saturday,
         'sunday': sunday,
         'holidaysOnly': holidays_only,
         'message': message,
      }

      if not success:
         response[ 'error' ] = (
            f'Could not replace opening schedule overlaps for "{ attraction }".'
         )

      handler._write_json( response )


   @staticmethod
   def trim_attraction_opening_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      attraction = data.get( 'attraction' )
      schedule_start_date = data.get( 'scheduleStartDate' )
      schedule_end_date = data.get( 'scheduleEndDate' )
      monday = data.get( 'monday' )
      tuesday = data.get( 'tuesday' )
      wednesday = data.get( 'wednesday' )
      thursday = data.get( 'thursday' )
      friday = data.get( 'friday' )
      saturday = data.get( 'saturday' )
      sunday = data.get( 'sunday' )
      holidays_only = data.get( 'holidaysOnly' )
      message = data.get( 'message' )

      success = AttractionCoordinator.trim_attraction_opening_schedule_overlaps(
         attraction=attraction,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )

      response = {
         'success': success,
         'attraction': attraction,
         'scheduleStartDate': schedule_start_date,
         'scheduleEndDate': schedule_end_date,
         'monday': monday,
         'tuesday': tuesday,
         'wednesday': wednesday,
         'thursday': thursday,
         'friday': friday,
         'saturday': saturday,
         'sunday': sunday,
         'holidaysOnly': holidays_only,
         'message': message,
      }

      if not success:
         response[ 'error' ] = (
            f'Could not trim opening schedule overlaps for "{ attraction }".'
         )

      handler._write_json( response )


   @staticmethod
   def _attraction_hours_schedule_payload( data: dict ) -> dict:
      return {
         'attraction': data.get( 'attraction' ),
         'start_date': data.get( 'scheduleStartDate' ),
         'end_date': data.get( 'scheduleEndDate' ),
         'weekday_start_time': data.get( 'weekdayStartTime' ),
         'weekday_end_time': data.get( 'weekdayEndTime' ),
         'weekend_holiday_start_time': data.get( 'weekendHolidayStartTime' ),
         'weekend_holiday_end_time': data.get( 'weekendHolidayEndTime' ),
      }


   @staticmethod
   def _attraction_hours_schedule_response(
         data: dict,
         *,
         success: bool,
         error: str | None = None,
         error_type: str | None = None ) -> dict:
      response = {
         'success': success,
         'attraction': data.get( 'attraction' ),
         'scheduleStartDate': data.get( 'scheduleStartDate' ),
         'scheduleEndDate': data.get( 'scheduleEndDate' ),
         'weekdayStartTime': data.get( 'weekdayStartTime' ),
         'weekdayEndTime': data.get( 'weekdayEndTime' ),
         'weekendHolidayStartTime': data.get( 'weekendHolidayStartTime' ),
         'weekendHolidayEndTime': data.get( 'weekendHolidayEndTime' ),
      }

      if error:
         response[ 'error' ] = error

      if error_type:
         response[ 'errorType' ] = error_type

      return response


   @staticmethod
   def get_attraction_hours_schedule_time_bounds(
         handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      try:
         bounds = AttractionCoordinator.get_attraction_hours_schedule_time_bounds(
            start_date=data.get( 'scheduleStartDate' ),
            end_date=data.get( 'scheduleEndDate' ) )
      except ValueError as error:
         handler._write_json( {
            'success': False,
            'error': str( error ),
         } )
         return

      handler._write_json( {
         'success': True,
         'weekday': {
            'openTime': DateValues.normalize_schedule_time(
               bounds.weekday.open_time ),
            'closeTime': DateValues.normalize_schedule_time(
               bounds.weekday.close_time ),
            'operatingDate': bounds.weekday.operating_date,
         },
         'weekendHoliday': {
            'openTime': DateValues.normalize_schedule_time(
               bounds.weekend_holiday.open_time ),
            'closeTime': DateValues.normalize_schedule_time(
               bounds.weekend_holiday.close_time ),
            'operatingDate': bounds.weekend_holiday.operating_date,
         },
      } )


   @staticmethod
   def set_attraction_hours_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      payload = AttractionController._attraction_hours_schedule_payload( data )

      try:
         success = AttractionCoordinator.set_attraction_hours_schedule( **payload )
      except ValueError as error:
         handler._write_json(
            AttractionController._attraction_hours_schedule_response(
               data,
               success=False,
               error=str( error ),
               error_type='invalidAttractionHours' ) )
         return

      response = AttractionController._attraction_hours_schedule_response(
         data,
         success=success )

      if not success:
         response[ 'error' ] = (
            f'Could not set attraction hours for "{ payload[ "attraction" ] }".'
         )
         response[ 'errorType' ] = 'overlappingSchedule'

      handler._write_json( response )


   @staticmethod
   def replace_attraction_hours_schedule_overlaps(
         handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      payload = AttractionController._attraction_hours_schedule_payload( data )

      try:
         success = AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
            **payload )
      except ValueError as error:
         handler._write_json(
            AttractionController._attraction_hours_schedule_response(
               data,
               success=False,
               error=str( error ),
               error_type='invalidAttractionHours' ) )
         return

      response = AttractionController._attraction_hours_schedule_response(
         data,
         success=success )

      if not success:
         response[ 'error' ] = (
            f'Could not replace attraction hours overlaps for '
            f'"{ payload[ "attraction" ] }".'
         )

      handler._write_json( response )


   @staticmethod
   def trim_attraction_hours_schedule_overlaps(
         handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      payload = AttractionController._attraction_hours_schedule_payload( data )

      try:
         success = AttractionCoordinator.trim_attraction_hours_schedule_overlaps(
            **payload )
      except ValueError as error:
         handler._write_json(
            AttractionController._attraction_hours_schedule_response(
               data,
               success=False,
               error=str( error ),
               error_type='invalidAttractionHours' ) )
         return

      response = AttractionController._attraction_hours_schedule_response(
         data,
         success=success )

      if not success:
         response[ 'error' ] = (
            f'Could not trim attraction hours overlaps for '
            f'"{ payload[ "attraction" ] }".'
         )

      handler._write_json( response )
