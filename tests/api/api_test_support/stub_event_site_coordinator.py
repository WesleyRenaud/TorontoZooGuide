from __future__ import annotations

from api.models.event_site import EventSite


class StubEventSiteCoordinator():
   instances: list[ StubEventSiteCoordinator ] = []


   def __init__( self, *, event_sites: list[ EventSite ] ) -> None:
      self.event_sites = event_sites
      self.calls: list[ tuple[ str, dict[ str, object ] ] ] = []
      StubEventSiteCoordinator.instances.append( self )


   def get_event_sites( self ) -> list[ EventSite ]:
      self.calls.append( ( 'get_event_sites', {} ) )
      return list( self.event_sites )
