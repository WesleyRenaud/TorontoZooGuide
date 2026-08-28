from __future__ import annotations

from ..coordinators.restroom_coordinator import RestroomCoordinator
from ...json_handler import JsonRequestHandler
from ...shared.api_error_response import ApiErrorResponseApplier
from ...shared.enums.api_error_type import ApiErrorType


class RestroomController():
   @staticmethod
   def get_restrooms( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restrooms = RestroomCoordinator.get_restrooms(
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ),
         include_closed_restrooms=data.get( 'includeClosedRestrooms' ) or False )

      handler._write_json( {
         'restrooms': [ restroom.to_dict() for restroom in restrooms ],
      } )


   @staticmethod
   def get_restroom_names( handler: JsonRequestHandler ) -> None:
      restrooms = RestroomCoordinator.get_restroom_names()

      handler._write_json( {
         'restrooms': restrooms,
      } )


   @staticmethod
   def set_restroom_closed( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restroom = data.get( 'restroom' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = RestroomCoordinator.set_restroom_as_closed(
         restroom=restroom,
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'restroom': restroom,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_SET_CLOSED, name=restroom )

      handler._write_json( response )


   @staticmethod
   def set_restroom_open( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restroom = data.get( 'restroom' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )

      success = RestroomCoordinator.set_restroom_as_open(
         restroom=restroom,
         start_date=start_date,
         end_date=end_date )

      response = {
         'success': success,
         'restroom': restroom,
         'startDate': start_date,
         'endDate': end_date,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_SET_OPEN, name=restroom )

      handler._write_json( response )


   @staticmethod
   def set_restroom_alert( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restroom = data.get( 'restroom' )
      alert_start_date = data.get( 'alertStartDate' )
      alert_end_date = data.get( 'alertEndDate' )
      message = data.get( 'message' )

      success = RestroomCoordinator.set_restroom_alert(
         restroom=restroom,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )

      response = {
         'success': success,
         'restroom': restroom,
         'alertStartDate': alert_start_date,
         'alertEndDate': alert_end_date,
         'message': message,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_SET_RESTROOM_ALERT, name=restroom )

      handler._write_json( response )


   @staticmethod
   def remove_restroom_alert( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restroom = data.get( 'restroom' )

      success = RestroomCoordinator.remove_restroom_alert( restroom=restroom )

      response = {
         'success': success,
         'restroom': restroom,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_REMOVE_RESTROOM_ALERT, name=restroom )

      handler._write_json( response )
