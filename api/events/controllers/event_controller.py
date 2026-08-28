from __future__ import annotations

from ..coordinators.event_coordinator import EventCoordinator
from ...json_request_handler import JsonRequestHandler
from ...shared.api_error_response_applier import ApiErrorResponseApplier
from ...shared.enums.api_error_type import ApiErrorType


class EventController():
   @staticmethod
   def get_events( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      events = EventCoordinator.get_events_for_visit_date(
         month=data.get( 'month' ),
         day=data.get( 'day' ),
         year=data.get( 'year' ) )

      handler._write_json( {
         'events': [ event.to_dict() for event in events ],
      } )


   @staticmethod
   def create_event( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      name = data.get( 'name' )
      location = data.get( 'location' )
      description = data.get( 'description' )
      link = data.get( 'link' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )

      success = EventCoordinator.create_event(
         name=name,
         location=location,
         description=description,
         link=link,
         start_date=start_date,
         end_date=end_date )

      response = {
         'success': success,
         'name': name,
         'location': location,
         'description': description,
         'link': link,
         'startDate': start_date,
         'endDate': end_date,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_CREATE_EVENT )

      handler._write_json( response )
