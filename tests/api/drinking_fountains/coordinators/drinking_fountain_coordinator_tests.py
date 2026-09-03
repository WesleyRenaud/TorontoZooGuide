from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pytest

from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
from api.drinking_fountains.data_access.drinking_fountain_provider import DrinkingFountainProvider
from api.drinking_fountains.data_access.drinking_fountain_status_provider import DrinkingFountainStatusProvider
from api.drinking_fountains.data_access.drinking_fountain_status_record import DrinkingFountainStatusRecord
from api.drinking_fountains.domain.drinking_fountain_builder import DrinkingFountainBuilder
from api.drinking_fountains.status.drinking_fountain_closed_status import DrinkingFountainClosedStatus
from api.drinking_fountains.status.drinking_fountain_open_status import DrinkingFountainOpenStatus
from api.drinking_fountains.status.drinking_fountain_status_builder import DrinkingFountainStatusBuilder
from api.models.drinking_fountain import DrinkingFountain
from api.shared.calendar_dates import CalendarDates
from api.types import Types

VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026
VISIT_DATE = date( 2026, 6, 15 )
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Closed for the season.'
STATUS_LIKELIHOOD = 0.0
SEASONAL_LIKELIHOOD = 0.8

FOUNTAIN = DrinkingFountain(
   x_coord=10.0,
   y_coord=20.0,
   is_closed=False,
   closed_message=None,
   likelihood=80 )
STATUS_RECORD = DrinkingFountainStatusRecord(
   is_closed=True,
   start_date=START_DATE,
   end_date=END_DATE,
   closed_message=MESSAGE )
CLOSED_STATUS = DrinkingFountainClosedStatus(
   start_date=START_DATE,
   end_date=END_DATE,
   message=MESSAGE )
OPEN_STATUS = DrinkingFountainOpenStatus(
   start_date=START_DATE,
   end_date=END_DATE )


@dataclass
class StubRecord():
   pass


def Test_GetDrinkingFountains_TestStatusApplies_ExpectStatusBuilt(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   fountain_records = [ StubRecord() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      CalendarDates,
      'visit_target_date',
      lambda **_kwargs: VISIT_DATE )
   monkeypatch.setattr(
      DrinkingFountainStatusProvider,
      'fetch_drinking_fountain_status_record',
      lambda _conn: STATUS_RECORD )
   monkeypatch.setattr(
      DrinkingFountainStatusBuilder,
      'applies_to_date',
      lambda record, target_date: record is STATUS_RECORD and target_date == VISIT_DATE )
   monkeypatch.setattr(
      DrinkingFountainStatusBuilder,
      'build_status',
      lambda record: ( True, MESSAGE, STATUS_LIKELIHOOD ) if record is STATUS_RECORD else ( False, None, 1.0 ) )
   monkeypatch.setattr(
      DrinkingFountainProvider,
      'fetch_drinking_fountain_records',
      lambda _conn: fountain_records )

   def build_drinking_fountains(
         records: list[ StubRecord ],
         is_closed: bool,
         closed_message: str | None,
         likelihood: float ) -> list[ DrinkingFountain ]:
      captured[ 'records' ] = records
      captured[ 'is_closed' ] = is_closed
      captured[ 'closed_message' ] = closed_message
      captured[ 'likelihood' ] = likelihood
      return [ FOUNTAIN ]

   monkeypatch.setattr(
      DrinkingFountainBuilder,
      'build_drinking_fountains',
      build_drinking_fountains )

   assert DrinkingFountainCoordinator.get_drinking_fountains(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == [ FOUNTAIN ]
   assert captured[ 'records' ] is fountain_records
   assert captured[ 'is_closed' ] is True
   assert captured[ 'closed_message' ] == MESSAGE
   assert captured[ 'likelihood' ] == STATUS_LIKELIHOOD


def Test_GetDrinkingFountains_TestStatusMissing_ExpectSeasonalFallback(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   fountain_records = [ StubRecord() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      CalendarDates,
      'visit_target_date',
      lambda **_kwargs: VISIT_DATE )
   monkeypatch.setattr(
      DrinkingFountainStatusProvider,
      'fetch_drinking_fountain_status_record',
      lambda _conn: None )
   monkeypatch.setattr(
      DrinkingFountainStatusProvider,
      'fetch_drinking_fountain_seasonal_likelihood',
      lambda _conn, target_date: SEASONAL_LIKELIHOOD if target_date == VISIT_DATE else 0.0 )
   monkeypatch.setattr(
      DrinkingFountainStatusBuilder,
      'build_seasonal_status',
      lambda likelihood: ( False, None, likelihood ) )
   monkeypatch.setattr(
      DrinkingFountainProvider,
      'fetch_drinking_fountain_records',
      lambda _conn: fountain_records )

   def build_drinking_fountains(
         records: list[ StubRecord ],
         is_closed: bool,
         closed_message: str | None,
         likelihood: float ) -> list[ DrinkingFountain ]:
      captured[ 'records' ] = records
      captured[ 'is_closed' ] = is_closed
      captured[ 'closed_message' ] = closed_message
      captured[ 'likelihood' ] = likelihood
      return [ FOUNTAIN ]

   monkeypatch.setattr(
      DrinkingFountainBuilder,
      'build_drinking_fountains',
      build_drinking_fountains )

   assert DrinkingFountainCoordinator.get_drinking_fountains(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == [ FOUNTAIN ]
   assert captured[ 'records' ] is fountain_records
   assert captured[ 'is_closed' ] is False
   assert captured[ 'closed_message' ] is None
   assert captured[ 'likelihood' ] == SEASONAL_LIKELIHOOD


def Test_SetDrinkingFountainsAsClosed_TestBuilderAndProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ DrinkingFountainClosedStatus ] = []

   monkeypatch.setattr(
      DrinkingFountainStatusBuilder,
      'build_closed_status',
      lambda **_kwargs: CLOSED_STATUS )
   monkeypatch.setattr(
      DrinkingFountainStatusProvider,
      'save_drinking_fountain_closed_status',
      lambda _conn, *, status: saved.append( status ) or True )

   assert DrinkingFountainCoordinator.set_drinking_fountains_as_closed(
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE ) is True
   assert saved == [ CLOSED_STATUS ]


def Test_SetDrinkingFountainsAsOpen_TestBuilderAndProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ DrinkingFountainOpenStatus ] = []

   monkeypatch.setattr(
      DrinkingFountainStatusBuilder,
      'build_open_status',
      lambda **_kwargs: OPEN_STATUS )
   monkeypatch.setattr(
      DrinkingFountainStatusProvider,
      'save_drinking_fountain_open_status',
      lambda _conn, *, status: saved.append( status ) or True )

   assert DrinkingFountainCoordinator.set_drinking_fountains_as_open(
      start_date=START_DATE,
      end_date=END_DATE ) is True
   assert saved == [ OPEN_STATUS ]
