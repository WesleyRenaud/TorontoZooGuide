from __future__ import annotations

from ..coordinators.restroom_coordinator import RestroomCoordinator
from ...json_handler import JsonRequestHandler


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
         response[ 'error' ] = f'Could not set "{ restroom }" as closed.'

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
         response[ 'error' ] = f'Could not set "{ restroom }" as open.'

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
         response[ 'error' ] = f'Could not set alert for "{ restroom }".'

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
         response[ 'error' ] = f'Could not remove alert for "{ restroom }".'

      handler._write_json( response )
