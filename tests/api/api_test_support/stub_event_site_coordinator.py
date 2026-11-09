from __future__ import annotations

from api_test_support.coordinator_call import CoordinatorCall

from api.models.event_site import EventSite


class StubEventSiteCoordinator():
   instances: list[ StubEventSiteCoordinator ] = []
   event_sites: list[ EventSite ]
   calls: list[ CoordinatorCall ]


   def __init__( self, *, event_sites: list[ EventSite ] ) -> None:
      self.event_sites = event_sites
      self.calls = []
      StubEventSiteCoordinator.instances.append( self )


   def get_event_sites( self ) -> list[ EventSite ]:
      self.calls.append( CoordinatorCall( 'get_event_sites', {} ) )
      return list( self.event_sites )
