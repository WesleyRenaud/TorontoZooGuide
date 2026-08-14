from __future__ import annotations

from ..coordinators.zoomobile_coordinator import ZoomobileCoordinator
from ...json_handler import JsonRequestHandler


class ZoomobileController():
   @staticmethod
   def get_zoomobile_route( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      zoomobile_route = ZoomobileCoordinator.get_zoomobile_route(
         route=data.get( 'zoomobileRoute' ),
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ),
         zoomobile_stations_to_include=data.get( 'zoomobileStationsToInclude' ) or [] )

      handler._write_json( zoomobile_route.to_dict() )


   @staticmethod
   def get_zoomobile_station_names( handler: JsonRequestHandler ) -> None:
      zoomobile_stations = ZoomobileCoordinator.get_zoomobile_station_names()

      handler._write_json( {
         'zoomobile_stations': zoomobile_stations,
      } )


   @staticmethod
   def set_zoomobile_station_closed( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      zoomobile_station = data.get( 'zoomobileStation' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = ZoomobileCoordinator.set_zoomobile_station_as_closed(
         zoomobile_station=zoomobile_station,
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'zoomobile_station': zoomobile_station,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set "{ zoomobile_station }" as closed.'

      handler._write_json( response )


   @staticmethod
   def set_zoomobile_station_open( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      zoomobile_station = data.get( 'zoomobileStation' )

      success = ZoomobileCoordinator.set_zoomobile_station_as_open(
         zoomobile_station=zoomobile_station )

      response = {
         'success': success,
         'zoomobile_station': zoomobile_station,
      }

      if not success:
         response[ 'error' ] = f'Could not set "{ zoomobile_station }" as open.'

      handler._write_json( response )


   @staticmethod
   def set_current_zoomobile_route( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      route = data.get( 'route' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )

      success = ZoomobileCoordinator.set_current_zoomobile_route(
         route=route,
         start_date=start_date,
         end_date=end_date )

      response = {
         'success': success,
         'route': route,
         'startDate': start_date,
         'endDate': end_date,
      }

      if not success:
         response[ 'error' ] = f'Could not set Zoomobile route to "{ route }".'

      handler._write_json( response )
