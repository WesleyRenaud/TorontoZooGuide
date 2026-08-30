from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_emergency_intercom_coordinator import StubEmergencyIntercomCoordinator
import pytest

from api.emergency_intercoms.coordinators.emergency_intercom_coordinator import EmergencyIntercomCoordinator
import api.http_request_handler as server
from api.models.emergency_intercom import EmergencyIntercom


def _sample_emergency_intercom() -> EmergencyIntercom:
   return EmergencyIntercom( x_coord=23.456, y_coord=78.901 )


@pytest.fixture
def stub_emergency_intercom_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubEmergencyIntercomCoordinator:
   StubEmergencyIntercomCoordinator.instances = []
   stub = StubEmergencyIntercomCoordinator(
      emergency_intercoms=[ _sample_emergency_intercom() ] )
   patch_coordinator_with_stub( monkeypatch, EmergencyIntercomCoordinator, stub )
   return stub


def Test_GetEmergencyIntercoms_TestHttpRequest_ExpectReturnsEmergencyIntercoms(
      stub_emergency_intercom_coordinator: StubEmergencyIntercomCoordinator ) -> None:
   handler = make_handler( '/get-emergency-intercoms', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_emergency_intercom_coordinator.calls == [ ( 'get_emergency_intercoms', {} ) ]
   assert result[ 'emergency_intercoms' ] == [ _sample_emergency_intercom().to_dict() ]
