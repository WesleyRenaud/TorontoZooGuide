from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pytest

from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
from api.drinking_fountains.data_access.drinking_fountain_provider import DrinkingFountainProvider
from api.drinking_fountains.data_access.drinking_fountain_status_provider import DrinkingFountainStatusProvider
from api.drinking_fountains.data_access.drinking_fountain_status_record import DrinkingFountainStatusRecord
from api.drinking_fountains.domain.drinking_fountain_builder import DrinkingFountainBuilder
from api.drinking_fountains.domain.seasonal_drinking_fountains import SeasonalDrinkingFountains
from api.drinking_fountains.domain.seasonal_drinking_fountains_builder import SeasonalDrinkingFountainsBuilder
from api.drinking_fountains.status.drinking_fountain_closed_status import DrinkingFountainClosedStatus
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
         likelihood: float,
         is_closed_for_season: bool = False ) -> list[ DrinkingFountain ]:
      captured[ 'records' ] = records
      captured[ 'is_closed' ] = is_closed
      captured[ 'closed_message' ] = closed_message
      captured[ 'likelihood' ] = likelihood
      captured[ 'is_closed_for_season' ] = is_closed_for_season
      return [ FOUNTAIN ]

   monkeypatch.setattr(
      DrinkingFountainBuilder,
      'build_drinking_fountains',
      build_drinking_fountains )

   fountains = DrinkingFountainCoordinator.get_drinking_fountains(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR )

   assert fountains == [ FOUNTAIN ]
   assert captured[ 'records' ] is fountain_records
   assert captured[ 'is_closed' ] is True
   assert captured[ 'closed_message' ] == MESSAGE
   assert captured[ 'likelihood' ] == STATUS_LIKELIHOOD
   assert captured[ 'is_closed_for_season' ] is True


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
         likelihood: float,
         is_closed_for_season: bool = False ) -> list[ DrinkingFountain ]:
      captured[ 'records' ] = records
      captured[ 'is_closed' ] = is_closed
      captured[ 'closed_message' ] = closed_message
      captured[ 'likelihood' ] = likelihood
      captured[ 'is_closed_for_season' ] = is_closed_for_season
      return [ FOUNTAIN ]

   monkeypatch.setattr(
      DrinkingFountainBuilder,
      'build_drinking_fountains',
      build_drinking_fountains )

   fountains = DrinkingFountainCoordinator.get_drinking_fountains(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR )

   assert fountains == [ FOUNTAIN ]
   assert captured[ 'records' ] is fountain_records
   assert captured[ 'is_closed' ] is False
   assert captured[ 'closed_message' ] is None
   assert captured[ 'likelihood' ] == SEASONAL_LIKELIHOOD
   assert captured[ 'is_closed_for_season' ] is False


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

   saved_closed = DrinkingFountainCoordinator.set_drinking_fountains_as_closed(
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE )

   assert saved_closed is True
   assert saved == [ CLOSED_STATUS ]


def Test_SetDrinkingFountainsAsOpen_TestProvider_ExpectDeleted(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   deleted: list[ bool ] = []

   monkeypatch.setattr(
      DrinkingFountainStatusProvider,
      'delete_drinking_fountain_status',
      lambda _conn: deleted.append( True ) or True )

   saved_open = DrinkingFountainCoordinator.set_drinking_fountains_as_open()

   assert saved_open is True
   assert deleted == [ True ]


def Test_GetSeasonalDrinkingFountains_TestStatus_ExpectBuilt(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   built = SeasonalDrinkingFountains(
      is_closed=True,
      start=date( 2026, 11, 2 ),
      end=None,
   )
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      DrinkingFountainStatusProvider,
      'fetch_current_drinking_fountain_status_record',
      lambda _conn: STATUS_RECORD )

   def build( record: DrinkingFountainStatusRecord ) -> SeasonalDrinkingFountains:
      captured[ 'record' ] = record
      return built

   monkeypatch.setattr( SeasonalDrinkingFountainsBuilder, 'build', build )

   result = DrinkingFountainCoordinator.get_seasonal_drinking_fountains()

   assert result is built
   assert captured[ 'record' ] is STATUS_RECORD


def Test_GetSeasonalDrinkingFountains_TestOpenRecord_ExpectOpen(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      DrinkingFountainStatusProvider,
      'fetch_current_drinking_fountain_status_record',
      lambda _conn: DrinkingFountainStatusRecord(
         is_closed=False,
         start_date=None,
         end_date=None,
         closed_message=None,
      ) )

   status = DrinkingFountainCoordinator.get_seasonal_drinking_fountains()

   assert status == SeasonalDrinkingFountains(
      is_closed=False,
      start=None,
      end=None,
   )
