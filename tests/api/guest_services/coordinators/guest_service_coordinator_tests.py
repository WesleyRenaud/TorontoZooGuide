from __future__ import annotations

import pytest

from api.guest_services.coordinators.guest_service_coordinator import GuestServiceCoordinator
from api.guest_services.data_access.guest_service_provider import GuestServiceProvider
from api.models.guest_service import GuestService
from api.types import Types

GUEST_SERVICE = GuestService( service_type='First Aid', x_coord=5.5, y_coord=6.5 )


def Test_GetGuestServices_TestProviderRecords_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuestServiceProvider,
      'fetch_guest_services',
      lambda _conn: [ GUEST_SERVICE ] )

   assert GuestServiceCoordinator.get_guest_services() == [ GUEST_SERVICE ]
