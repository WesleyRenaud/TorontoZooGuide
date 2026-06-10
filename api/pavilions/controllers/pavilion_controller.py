from __future__ import annotations

from ..coordinators.pavilion_coordinator import PavilionCoordinator
from ...json_handler import JsonRequestHandler


class PavilionController():
   @staticmethod
   def get_pavilions( handler: JsonRequestHandler ) -> None:
      pavilions = PavilionCoordinator.get_pavilions()

      handler._write_json( {
         'pavilions': [ pavilion.to_dict() for pavilion in pavilions ],
      } )
