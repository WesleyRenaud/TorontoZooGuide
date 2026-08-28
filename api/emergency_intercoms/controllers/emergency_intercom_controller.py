from __future__ import annotations

from ..coordinators.emergency_intercom_coordinator import EmergencyIntercomCoordinator
from ...json_request_handler import JsonRequestHandler


class EmergencyIntercomController():
   @staticmethod
   def get_emergency_intercoms( handler: JsonRequestHandler ) -> None:
      emergency_intercoms = EmergencyIntercomCoordinator.get_emergency_intercoms()

      handler._write_json( {
         'emergency_intercoms': [
            emergency_intercom.to_dict() for emergency_intercom in emergency_intercoms
         ],
      } )
