from __future__ import annotations

from ..coordinators.transportation_coordinator import TransportationCoordinator
from ...json_handler import JsonRequestHandler


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
