from __future__ import annotations

from ..coordinators.event_site_coordinator import EventSiteCoordinator
from ...json_request_handler import JsonRequestHandler


class EventSiteController():
   @staticmethod
   def get_event_sites( handler: JsonRequestHandler ) -> None:
      event_sites = EventSiteCoordinator.get_event_sites()

      handler._write_json( {
         'event_sites': [ event_site.to_dict() for event_site in event_sites ],
      } )
