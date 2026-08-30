from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_defibrillator_coordinator import StubDefibrillatorCoordinator
import pytest

from api.defibrillators.coordinators.defibrillator_coordinator import DefibrillatorCoordinator
import api.http_request_handler as server
from api.models.defibrillator import Defibrillator


def _sample_defibrillator() -> Defibrillator:
   return Defibrillator( x_coord=12.345, y_coord=67.890 )


@pytest.fixture
def stub_defibrillator_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubDefibrillatorCoordinator:
   StubDefibrillatorCoordinator.instances = []
   stub = StubDefibrillatorCoordinator( defibrillators=[ _sample_defibrillator() ] )
   patch_coordinator_with_stub( monkeypatch, DefibrillatorCoordinator, stub )
   return stub


def Test_GetDefibrillators_TestHttpRequest_ExpectReturnsDefibrillators(
      stub_defibrillator_coordinator: StubDefibrillatorCoordinator ) -> None:
   handler = make_handler( '/get-defibrillators', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_defibrillator_coordinator.calls == [ ( 'get_defibrillators', {} ) ]
   assert result[ 'defibrillators' ] == [ _sample_defibrillator().to_dict() ]
