from __future__ import annotations

from ..data_access.event_site_provider import EventSiteProvider
from ...models import EventSite
from ...request_connection_provider import RequestConnectionProvider


class EventSiteCoordinator():
   @classmethod
   def get_event_sites( cls ) -> list[ EventSite ]:
      return EventSiteProvider.fetch_event_sites( RequestConnectionProvider.get() )
