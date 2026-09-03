from __future__ import annotations

import pytest

from api.emergency_intercoms.coordinators.emergency_intercom_coordinator import EmergencyIntercomCoordinator
from api.emergency_intercoms.data_access.emergency_intercom_provider import EmergencyIntercomProvider
from api.models.emergency_intercom import EmergencyIntercom
from api.types import Types

EMERGENCY_INTERCOM = EmergencyIntercom( x_coord=1.0, y_coord=2.0 )


def Test_GetEmergencyIntercoms_TestProviderRecords_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      EmergencyIntercomProvider,
      'fetch_emergency_intercoms',
      lambda _conn: [ EMERGENCY_INTERCOM ] )

   assert EmergencyIntercomCoordinator.get_emergency_intercoms() == [ EMERGENCY_INTERCOM ]
