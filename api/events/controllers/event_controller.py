from __future__ import annotations

from ..coordinators.event_coordinator import EventCoordinator
from ...json_handler import JsonRequestHandler


class EventController():
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
         response[ 'error' ] = 'Could not create event.'

      handler._write_json( response )
