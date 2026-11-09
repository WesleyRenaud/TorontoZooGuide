from __future__ import annotations

from api_test_support.coordinator_call import CoordinatorCall

from api.models.picnic_site import PicnicSite


class StubPicnicSiteCoordinator():
   instances: list[ StubPicnicSiteCoordinator ] = []
   picnic_sites: list[ PicnicSite ]
   calls: list[ CoordinatorCall ]


   def __init__( self, *, picnic_sites: list[ PicnicSite ] ) -> None:
      self.picnic_sites = picnic_sites
      self.calls = []
      StubPicnicSiteCoordinator.instances.append( self )


   def get_picnic_sites( self ) -> list[ PicnicSite ]:
      self.calls.append( CoordinatorCall( 'get_picnic_sites', {} ) )
      return list( self.picnic_sites )
