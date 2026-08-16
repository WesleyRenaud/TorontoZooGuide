from __future__ import annotations

from ..coordinators.transportation_coordinator import TransportationCoordinator
from ...json_handler import JsonRequestHandler


class TransportationController():
   @staticmethod
   def get_transportations( handler: JsonRequestHandler ) -> None:
      handler._write_json( {
         'transportations': [
            transportation.to_dict()
            for transportation
            in TransportationCoordinator.get_transportations()
         ],
      } )


   @staticmethod
   def get_transportation_routes( handler: JsonRequestHandler ) -> None:
      handler._write_json( {
         'transportations': TransportationCoordinator.get_transportation_routes(),
      } )
