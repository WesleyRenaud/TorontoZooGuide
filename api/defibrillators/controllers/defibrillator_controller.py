from __future__ import annotations

from ..coordinators.defibrillator_coordinator import DefibrillatorCoordinator
from ...json_handler import JsonRequestHandler


class DefibrillatorController():


   @staticmethod
   def get_defibrillators( handler: JsonRequestHandler ) -> None:
      defibrillators = DefibrillatorCoordinator.get_defibrillators()

      handler._write_json( {
         'defibrillators': [ defibrillator.to_dict() for defibrillator in defibrillators ],
      } )
