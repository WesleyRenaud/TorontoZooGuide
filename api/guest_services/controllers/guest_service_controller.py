from __future__ import annotations

from ..coordinators.guest_service_coordinator import GuestServiceCoordinator
from ...json_handler import JsonRequestHandler


class GuestServiceController():
   @staticmethod
   def get_guest_services( handler: JsonRequestHandler ) -> None:
      guest_services = GuestServiceCoordinator.get_guest_services()

      handler._write_json( {
         'guest_services': [ guest_service.to_dict() for guest_service in guest_services ],
      } )
