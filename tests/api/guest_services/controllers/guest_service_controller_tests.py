from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_guest_service_coordinator import StubGuestServiceCoordinator
import pytest

from api.guest_services.coordinators.guest_service_coordinator import GuestServiceCoordinator
import api.http_request_handler as server
from api.models.guest_service import GuestService


def _sample_guest_service() -> GuestService:
   return GuestService(
      service_type='Information',
      x_coord=34.567,
      y_coord=89.012 )


@pytest.fixture
def stub_guest_service_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubGuestServiceCoordinator:
   StubGuestServiceCoordinator.instances = []
   stub = StubGuestServiceCoordinator( guest_services=[ _sample_guest_service() ] )
   patch_coordinator_with_stub( monkeypatch, GuestServiceCoordinator, stub )
   return stub


def Test_GetGuestServices_TestHttpRequest_ExpectReturnsGuestServices(
      stub_guest_service_coordinator: StubGuestServiceCoordinator ) -> None:
   handler = make_handler( '/get-guest-services', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_guest_service_coordinator.calls == [ ( 'get_guest_services', {} ) ]
   assert result[ 'guest_services' ] == [ _sample_guest_service().to_dict() ]
