from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_picnic_site_coordinator import StubPicnicSiteCoordinator
import pytest

import api.http_request_handler as server
from api.models.picnic_site import PicnicSite
from api.picnic_sites.coordinators.picnic_site_coordinator import PicnicSiteCoordinator


def _sample_picnic_site() -> PicnicSite:
   return PicnicSite( x_coord=45.678, y_coord=90.123 )


@pytest.fixture
def stub_picnic_site_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubPicnicSiteCoordinator:
   StubPicnicSiteCoordinator.instances = []
   stub = StubPicnicSiteCoordinator( picnic_sites=[ _sample_picnic_site() ] )
   patch_coordinator_with_stub( monkeypatch, PicnicSiteCoordinator, stub )
   return stub


def Test_GetPicnicSites_TestHttpRequest_ExpectReturnsPicnicSites(
      stub_picnic_site_coordinator: StubPicnicSiteCoordinator ) -> None:
   handler = make_handler( '/get-picnic-sites', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_picnic_site_coordinator.calls == [ ( 'get_picnic_sites', {} ) ]
   assert result[ 'picnic_sites' ] == [ _sample_picnic_site().to_dict() ]
