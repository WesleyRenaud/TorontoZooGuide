from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import pytest

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.data_access.guardians_talk_occurrence_provider import GuardiansTalkOccurrenceProvider
from api.guardians.data_access.guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from api.guardians.occurrences.guardians_talk_occurrence_input import GuardiansTalkOccurrenceInput
from api.request_connection_provider import RequestConnectionProvider
from api.shared.api_operation_failure import ApiOperationFailure
from api.shared.enums.api_error_type import ApiErrorType
from api.types import Types


TALK_NAME = 'African Lion'
TALK_LOCATION = 'Africa Savanna'
OCCURRENCE_DATE = '2026-06-15'
TALK_TIME = '10:00 AM'
ADDED_TALK_TIME = '11:00 AM'


@dataclass
class StubConnection():
   pass


STUB_CONNECTION = cast( Types.Connection, StubConnection() )


@pytest.fixture
def stub_request_connection( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: STUB_CONNECTION )


def Test_AddGuardiansTalkOccurrence_TestExistingOccurrence_ExpectAlreadyExistsFailure(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   def occurrence_exists(
         _conn: Types.Connection,
         talk_name: str,
         location: str,
         occurrence_date: Types.DateKey,
         talk_time: str,
   ) -> bool:
      return (
         talk_name == TALK_NAME
         and location == TALK_LOCATION
         and occurrence_date == OCCURRENCE_DATE
         and talk_time == TALK_TIME )

   monkeypatch.setattr(
      GuardiansTalkOccurrenceProvider,
      'occurrence_exists',
      occurrence_exists )

   success, failure = GuardiansCoordinator.add_guardians_talk_occurrence(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      date=OCCURRENCE_DATE,
      talk_times=[ TALK_TIME ] )

   assert success is False
   assert failure == ApiOperationFailure(
      error_type=ApiErrorType.GUARDIANS_TALK_OCCURRENCE_ALREADY_EXISTS,
      params={
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'date': OCCURRENCE_DATE,
         'talkTime': TALK_TIME,
      } )


def Test_AddGuardiansTalkOccurrence_TestNewOccurrence_ExpectSaved(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   saved_talk_times: list[ str ] = []

   monkeypatch.setattr(
      GuardiansTalkOccurrenceProvider,
      'occurrence_exists',
      lambda *_args, **_kwargs: False )

   def save_occurrence(
         _conn: Types.Connection,
         occurrence: GuardiansTalkOccurrenceInput,
   ) -> bool:
      saved_talk_times.append( occurrence.talk_time )
      return True

   monkeypatch.setattr(
      GuardiansTalkOccurrenceProvider,
      'save_occurrence',
      save_occurrence )

   success, failure = GuardiansCoordinator.add_guardians_talk_occurrence(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      date=OCCURRENCE_DATE,
      talk_times=[ ADDED_TALK_TIME ] )

   assert success is True
   assert failure is None
   assert saved_talk_times == [ ADDED_TALK_TIME ]


def Test_GetGuardiansTalkScheduleTimes_TestUnsortedProviderTimes_ExpectSorted(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   monkeypatch.setattr(
      GuardiansTalkScheduleProvider,
      'fetch_schedule_times',
      lambda *_args, **_kwargs: [ '3:30 PM', '10:00 AM' ] )

   assert GuardiansCoordinator.get_guardians_talk_schedule_times(
      TALK_NAME,
      TALK_LOCATION ) == [ '10:00 AM', '3:30 PM' ]
