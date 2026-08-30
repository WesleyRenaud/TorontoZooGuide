from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_event_site_coordinator import StubEventSiteCoordinator
import pytest

from api.event_sites.coordinators.event_site_coordinator import EventSiteCoordinator
import api.http_request_handler as server
from api.models.event_site import EventSite


def _sample_event_site() -> EventSite:
   return EventSite(
      name='Special Events Center',
      x_coord=56.789,
      y_coord=12.345 )


@pytest.fixture
def stub_event_site_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubEventSiteCoordinator:
   StubEventSiteCoordinator.instances = []
   stub = StubEventSiteCoordinator( event_sites=[ _sample_event_site() ] )
   patch_coordinator_with_stub( monkeypatch, EventSiteCoordinator, stub )
   return stub


def Test_GetEventSites_TestHttpRequest_ExpectReturnsEventSites(
      stub_event_site_coordinator: StubEventSiteCoordinator ) -> None:
   handler = make_handler( '/get-event-sites', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_event_site_coordinator.calls == [ ( 'get_event_sites', {} ) ]
   assert result[ 'event_sites' ] == [ _sample_event_site().to_dict() ]
