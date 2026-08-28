from __future__ import annotations

from ..coordinators.update_coordinator import UpdateCoordinator
from ...json_request_handler import JsonRequestHandler
from ...shared.api_error_response_applier import ApiErrorResponseApplier
from ...shared.enums.api_error_type import ApiErrorType


class UpdateController():
   @staticmethod
   def get_updates( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      updates = UpdateCoordinator.get_updates_for_visit_date(
         month=data.get( 'month' ),
         day=data.get( 'day' ),
         year=data.get( 'year' ) )

      handler._write_json( {
         'updates': [ update.to_dict() for update in updates ],
      } )


   @staticmethod
   def get_active_update_options( handler: JsonRequestHandler ) -> None:
      updates = UpdateCoordinator.get_unexpired_updates()

      handler._write_json( {
         'updates': [ update.to_dict() for update in updates ],
      } )


   @staticmethod
   def create_update( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      title = data.get( 'title' )
      description = data.get( 'description' )
      update_type = data.get( 'type' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )

      success = UpdateCoordinator.create_update(
         title=title,
         description=description,
         update_type=update_type,
         start_date=start_date,
         end_date=end_date )

      response = {
         'success': success,
         'title': title,
         'description': description,
         'type': update_type,
         'startDate': start_date,
         'endDate': end_date,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_CREATE_UPDATE )

      handler._write_json( response )


   @staticmethod
   def end_update( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      title = data.get( 'title' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )

      success = UpdateCoordinator.end_update(
         title=title,
         start_date=start_date,
         end_date=end_date )

      response = {
         'success': success,
         'title': title,
         'startDate': start_date,
         'endDate': end_date,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_END_UPDATE )

      handler._write_json( response )


   @staticmethod
   def edit_update( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      title = data.get( 'title' )
      start_date = data.get( 'startDate' )
      description = data.get( 'description' )
      update_type = data.get( 'type' )
      end_date = data.get( 'endDate' )

      success = UpdateCoordinator.edit_update(
         title=title,
         start_date=start_date,
         description=description,
         update_type=update_type,
         end_date=end_date )

      response = {
         'success': success,
         'title': title,
         'startDate': start_date,
         'description': description,
         'type': update_type,
         'endDate': end_date,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_EDIT_UPDATE )

      handler._write_json( response )
