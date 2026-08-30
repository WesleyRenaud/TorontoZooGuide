from __future__ import annotations

from api.models.picnic_site import PicnicSite


class StubPicnicSiteCoordinator():
   instances: list[ StubPicnicSiteCoordinator ] = []


   def __init__( self, *, picnic_sites: list[ PicnicSite ] ) -> None:
      self.picnic_sites = picnic_sites
      self.calls: list[ tuple[ str, dict[ str, object ] ] ] = []
      StubPicnicSiteCoordinator.instances.append( self )


   def get_picnic_sites( self ) -> list[ PicnicSite ]:
      self.calls.append( ( 'get_picnic_sites', {} ) )
      return list( self.picnic_sites )
