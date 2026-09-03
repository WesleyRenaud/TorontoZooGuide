from __future__ import annotations

import pytest

from api.models.picnic_site import PicnicSite
from api.picnic_sites.coordinators.picnic_site_coordinator import PicnicSiteCoordinator
from api.picnic_sites.data_access.picnic_site_provider import PicnicSiteProvider
from api.types import Types

PICNIC_SITE = PicnicSite( x_coord=7.0, y_coord=8.0 )

def Test_GetPicnicSites_TestProviderRecords_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      PicnicSiteProvider,
      'fetch_picnic_sites',
      lambda _conn: [ PICNIC_SITE ] )

   assert PicnicSiteCoordinator.get_picnic_sites() == [ PICNIC_SITE ]
