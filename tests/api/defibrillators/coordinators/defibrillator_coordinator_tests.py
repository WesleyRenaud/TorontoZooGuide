from __future__ import annotations

import pytest

from api.defibrillators.coordinators.defibrillator_coordinator import DefibrillatorCoordinator
from api.defibrillators.data_access.defibrillator_provider import DefibrillatorProvider
from api.models.defibrillator import Defibrillator

DEFIBRILLATOR = Defibrillator( x_coord=12.5, y_coord=67.5 )


def Test_GetDefibrillators_TestProviderRecords_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      DefibrillatorProvider,
      'fetch_defibrillators',
      lambda _conn: [ DEFIBRILLATOR ] )

   assert DefibrillatorCoordinator.get_defibrillators() == [ DEFIBRILLATOR ]
