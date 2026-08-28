from __future__ import annotations

from ..coordinators.attraction_coordinator import AttractionCoordinator
from ...json_handler import JsonRequestHandler
from ...shared.api_error_response import ApiErrorResponseApplier
from ...shared.calendar_dates import DateValues
from ...shared.enums.api_error_type import ApiErrorType


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
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_SET_CLOSED, name=attraction )

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
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_CREATE_CLOSURE_OVERRIDE, name=attraction )

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
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_SET_OPENING_SCHEDULE, name=attraction )
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
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_REPLACE_OPENING_SCHEDULE_OVERLAPS, name=attraction )

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
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_TRIM_OPENING_SCHEDULE_OVERLAPS, name=attraction )

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
         success: bool ) -> dict:
      return {
         'success': success,
         'attraction': data.get( 'attraction' ),
         'scheduleStartDate': data.get( 'scheduleStartDate' ),
         'scheduleEndDate': data.get( 'scheduleEndDate' ),
         'weekdayStartTime': data.get( 'weekdayStartTime' ),
         'weekdayEndTime': data.get( 'weekdayEndTime' ),
         'weekendHolidayStartTime': data.get( 'weekendHolidayStartTime' ),
         'weekendHolidayEndTime': data.get( 'weekendHolidayEndTime' ),
      }


   @staticmethod
   def _invalid_attraction_hours_response( data: dict ) -> dict:
      response = AttractionController._attraction_hours_schedule_response(
         data,
         success=False )
      ApiErrorResponseApplier.apply_error( response, ApiErrorType.INVALID_ATTRACTION_HOURS )

      return response


   @staticmethod
   def get_attraction_hours_schedule_time_bounds(
         handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      try:
         bounds = AttractionCoordinator.get_attraction_hours_schedule_time_bounds(
            start_date=data.get( 'scheduleStartDate' ),
            end_date=data.get( 'scheduleEndDate' ) )
      except ValueError:
         response = { 'success': False }
         ApiErrorResponseApplier.apply_error(
            response,
            ApiErrorType.COULD_NOT_RESOLVE_ATTRACTION_HOURS_TIME_BOUNDS )
         handler._write_json( response )
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
      except ValueError:
         handler._write_json(
            AttractionController._invalid_attraction_hours_response( data ) )
         return

      response = AttractionController._attraction_hours_schedule_response(
         data,
         success=success )

      if not success:
         ApiErrorResponseApplier.apply_error(
            response,
            ApiErrorType.COULD_NOT_SET_ATTRACTION_HOURS,
            name=payload[ 'attraction' ] )
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
      except ValueError:
         handler._write_json(
            AttractionController._invalid_attraction_hours_response( data ) )
         return

      response = AttractionController._attraction_hours_schedule_response(
         data,
         success=success )

      if not success:
         ApiErrorResponseApplier.apply_error(
            response,
            ApiErrorType.COULD_NOT_REPLACE_ATTRACTION_HOURS_OVERLAPS,
            name=payload[ 'attraction' ] )

      handler._write_json( response )


   @staticmethod
   def trim_attraction_hours_schedule_overlaps(
         handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      payload = AttractionController._attraction_hours_schedule_payload( data )

      try:
         success = AttractionCoordinator.trim_attraction_hours_schedule_overlaps(
            **payload )
      except ValueError:
         handler._write_json(
            AttractionController._invalid_attraction_hours_response( data ) )
         return

      response = AttractionController._attraction_hours_schedule_response(
         data,
         success=success )

      if not success:
         ApiErrorResponseApplier.apply_error(
            response,
            ApiErrorType.COULD_NOT_TRIM_ATTRACTION_HOURS_OVERLAPS,
            name=payload[ 'attraction' ] )

      handler._write_json( response )
