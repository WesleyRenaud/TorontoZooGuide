from __future__ import annotations

from ..data_access.picnic_site_provider import PicnicSiteProvider
from ...models import PicnicSite
from ...request_connection_provider import RequestConnectionProvider


class PicnicSiteCoordinator():
   @classmethod
   def get_picnic_sites( cls ) -> list[ PicnicSite ]:
      return PicnicSiteProvider.fetch_picnic_sites( RequestConnectionProvider.get() )
