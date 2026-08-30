from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api_test_support.frozen_datetime import patch_database_today
import pytest

from api.updates.domain.update_type import UpdateType
from api.updates.operations.update_edit_input_builder import UpdateEditInputBuilder
from api.updates.operations.update_end_input_builder import UpdateEndInputBuilder


UPDATE_TITLE = 'Giraffe habitat update'
UPDATE_DESCRIPTION = 'Temporary viewing change.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
FROZEN_TODAY = date( 2026, 6, 15 )


@pytest.fixture
def freeze_database_today( monkeypatch: pytest.MonkeyPatch ) -> Callable[ [ date ], None ]:
   def freeze( value: date ) -> None:
      patch_database_today( monkeypatch, value )

   return freeze


def Test_BuildEditInput_TestValidPayload_ExpectNormalizedEditInput() -> None:
   edit_input = UpdateEditInputBuilder.build(
      title=UPDATE_TITLE,
      start_date=START_DATE,
      description=UPDATE_DESCRIPTION,
      update_type='New Arrival',
      end_date=END_DATE )

   assert edit_input.title == UPDATE_TITLE
   assert edit_input.description == UPDATE_DESCRIPTION
   assert edit_input.start_date == START_DATE
   assert edit_input.end_date == END_DATE
   assert edit_input.update_type == UpdateType.NEW_ARRIVAL.value


def Test_BuildEditInput_TestMissingEndDate_ExpectNoneEndDate() -> None:
   edit_input = UpdateEditInputBuilder.build(
      title=UPDATE_TITLE,
      start_date=START_DATE,
      description=UPDATE_DESCRIPTION,
      update_type='Closure',
      end_date=None )

   assert edit_input.end_date is None
   assert edit_input.update_type == UpdateType.CLOSURE.value


def Test_BuildEndInput_TestMissingEndDate_ExpectTodayDefault(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )

   end_input = UpdateEndInputBuilder.build(
      title=UPDATE_TITLE,
      start_date=START_DATE,
      end_date=None )

   assert end_input.title == UPDATE_TITLE
   assert end_input.start_date == START_DATE
   assert end_input.end_date == FROZEN_TODAY.isoformat()


def Test_BuildEndInput_TestProvidedEndDate_ExpectUnchangedEndDate() -> None:
   end_input = UpdateEndInputBuilder.build(
      title=UPDATE_TITLE,
      start_date=START_DATE,
      end_date=END_DATE )

   assert end_input.end_date == END_DATE
