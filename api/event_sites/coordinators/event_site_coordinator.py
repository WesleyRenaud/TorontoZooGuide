from __future__ import annotations

from ..data_access.event_site import fetch_event_sites
from ...models import EventSite
from ...request_connection import get_connection


class EventSiteCoordinator():
   @classmethod
   def get_event_sites( cls ) -> list[ EventSite ]:
      return fetch_event_sites( get_connection() )
