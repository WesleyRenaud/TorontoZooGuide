from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_zoo_hours_coordinator import StubZooHoursCoordinator
import pytest

import api.http_request_handler as server
from api.models.zoo_hours import ZooHours
from api.zoo_hours.coordinators.zoo_hours_coordinator import ZooHoursCoordinator


VISIT_MONTH = 'June'
VISIT_DAY = 20
VISIT_YEAR = 2026


def _sample_zoo_hours() -> ZooHours:
   return ZooHours(
      date='2026-06-20',
      early_admission_time='09:00',
      open_time='09:30',
      last_admission_time='18:00',
      close_time='19:00' )


@pytest.fixture
def stub_zoo_hours_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubZooHoursCoordinator:
   StubZooHoursCoordinator.instances = []
   stub = StubZooHoursCoordinator( zoo_hours=_sample_zoo_hours() )
   patch_coordinator_with_stub( monkeypatch, ZooHoursCoordinator, stub )
   return stub


def Test_GetZooHours_TestHttpRequest_ExpectMapsVisitDateAndReturnsHours(
      stub_zoo_hours_coordinator: StubZooHoursCoordinator ) -> None:
   handler = make_handler(
      '/get-zoo-hours',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_zoo_hours_coordinator.calls == [
      (
         'get_zoo_hours',
         {
            'day': VISIT_DAY,
            'month': VISIT_MONTH,
            'year': VISIT_YEAR,
         }
      )
   ]
   assert result[ 'hours' ] == _sample_zoo_hours().to_dict()


def Test_GetZooHours_TestHttpRequest_ExpectNullWhenCoordinatorReturnsNone(
      stub_zoo_hours_coordinator: StubZooHoursCoordinator ) -> None:
   stub_zoo_hours_coordinator.zoo_hours = None
   handler = make_handler( '/get-zoo-hours', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'hours' ] is None
