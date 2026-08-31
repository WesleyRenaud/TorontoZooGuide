from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import pytest

from api.request_connection_provider import RequestConnectionProvider
from api.types import Types
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.data_access.wild_encounter_schedule_provider import WildEncounterScheduleProvider


WILD_ENCOUNTER_NAME = 'African Rainforest'


@dataclass
class StubConnection():
   pass


STUB_CONNECTION = cast( Types.Connection, StubConnection() )


@pytest.fixture
def stub_request_connection( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: STUB_CONNECTION )


def Test_GetWildEncounterScheduleTimes_TestUnsortedProviderTimes_ExpectSorted(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   monkeypatch.setattr(
      WildEncounterScheduleProvider,
      'fetch_schedule_times',
      lambda *_args, **_kwargs: [ '3:30 PM', '2:00 PM' ] )

   assert WildEncounterCoordinator.get_wild_encounter_schedule_times(
      WILD_ENCOUNTER_NAME ) == [ '2:00 PM', '3:30 PM' ]
