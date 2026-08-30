from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_pavilion_coordinator import StubPavilionCoordinator
import pytest

import api.http_request_handler as server
from api.models.pavilion import Pavilion
from api.pavilions.coordinators.pavilion_coordinator import PavilionCoordinator


PAVILION_NAME = 'African Rainforest Pavilion'
PAVILION_REGION = 'Africa'


def _sample_pavilion() -> Pavilion:
   return Pavilion(
      name=PAVILION_NAME,
      region=PAVILION_REGION,
      description='Indoor rainforest exhibit.',
      x_coord=10.0,
      y_coord=20.0 )


@pytest.fixture
def stub_pavilion_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubPavilionCoordinator:
   StubPavilionCoordinator.instances = []
   stub = StubPavilionCoordinator( pavilions=[ _sample_pavilion() ] )
   patch_coordinator_with_stub( monkeypatch, PavilionCoordinator, stub )
   return stub


def Test_GetPavilions_TestHttpRequest_ExpectReturnsPavilions(
      stub_pavilion_coordinator: StubPavilionCoordinator ) -> None:
   handler = make_handler( '/get-pavilions', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_pavilion_coordinator.calls == [ ( 'get_pavilions', {} ) ]
   assert result[ 'pavilions' ] == [ _sample_pavilion().to_dict() ]
