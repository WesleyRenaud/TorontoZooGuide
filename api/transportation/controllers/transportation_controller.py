from __future__ import annotations

from ..coordinators.transportation_coordinator import TransportationCoordinator
from ...json_request_handler import JsonRequestHandler
from ...shared.api_error_response_applier import ApiErrorResponseApplier
from ...shared.enums.api_error_type import ApiErrorType
from ...shared.enums.transportation_name import TransportationName


class TransportationController():
   @staticmethod
   def get_transportations( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      transportations = TransportationCoordinator.get_transportations(
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ) )

      handler._write_json( {
         'transportations': [
            transportation.to_dict()
            for transportation in transportations
         ],
      } )


   @staticmethod
   def get_transportation_routes( handler: JsonRequestHandler ) -> None:
      handler._write_json( {
         'transportations': TransportationCoordinator.get_transportation_routes(),
      } )


   @staticmethod
   def get_transportation_route( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      transportation = data.get( 'transportation' ) or TransportationName.ZOOMOBILE

      transportation_route = TransportationCoordinator.get_transportation_route(
         route=data.get( 'transportationRoute' ),
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ),
         transportation_stations_to_include=data.get( 'transportationStationsToInclude' ) or [],
         transportation=transportation )

      handler._write_json( transportation_route.to_dict() )


   @staticmethod
   def get_transportation_station_names( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      transportation = data.get( 'transportation' ) or TransportationName.ZOOMOBILE
      transportation_stations = TransportationCoordinator.get_transportation_station_names(
         transportation=transportation )

      handler._write_json( {
         'transportation_stations': transportation_stations,
      } )


   @staticmethod
   def set_transportation_station_closed( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      transportation = data.get( 'transportation' ) or TransportationName.ZOOMOBILE

      transportation_station = data.get( 'transportationStation' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = TransportationCoordinator.set_transportation_station_as_closed(
         transportation_station=transportation_station,
         start_date=start_date,
         end_date=end_date,
         message=message,
         transportation=transportation )

      response = {
         'success': success,
         'transportation_station': transportation_station,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_SET_CLOSED, name=transportation_station )

      handler._write_json( response )


   @staticmethod
   def set_transportation_station_open( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      transportation = data.get( 'transportation' ) or TransportationName.ZOOMOBILE

      transportation_station = data.get( 'transportationStation' )

      success = TransportationCoordinator.set_transportation_station_as_open(
         transportation_station=transportation_station,
         transportation=transportation )

      response = {
         'success': success,
         'transportation_station': transportation_station,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_SET_OPEN, name=transportation_station )

      handler._write_json( response )


   @staticmethod
   def set_current_transportation_route( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()
      transportation = data.get( 'transportation' ) or TransportationName.ZOOMOBILE

      route = data.get( 'route' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )

      success = TransportationCoordinator.set_current_transportation_route(
         route=route,
         start_date=start_date,
         end_date=end_date,
         transportation=transportation )

      response = {
         'success': success,
         'route': route,
         'startDate': start_date,
         'endDate': end_date,
      }

      if not success:
         ApiErrorResponseApplier.apply_error( response, ApiErrorType.COULD_NOT_SET_TRANSPORTATION_ROUTE, route=route )

      handler._write_json( response )
