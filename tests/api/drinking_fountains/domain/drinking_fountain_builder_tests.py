from __future__ import annotations

from datetime import date

from api.drinking_fountains.data_access.drinking_fountain_record import DrinkingFountainRecord
from api.drinking_fountains.data_access.drinking_fountain_status_record import DrinkingFountainStatusRecord
from api.drinking_fountains.domain.drinking_fountain_builder import DrinkingFountainBuilder
from api.drinking_fountains.status.drinking_fountain_status_builder import DrinkingFountainStatusBuilder


VISIT_DATE = date( 2026, 6, 15 )
OUTSIDE_VISIT_DATE = date( 2026, 7, 1 )
CLOSED_MESSAGE = 'Closed for testing.'
DEFAULT_CLOSED_MESSAGE = 'The drinking fountains are closed for the season.'


def Test_BuildClosedStatus_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   status = DrinkingFountainStatusBuilder.build_closed_status(
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='' )

   assert status.message == DEFAULT_CLOSED_MESSAGE


def Test_AppliesToDate_TestVisitDateInRange_ExpectTrue() -> None:
   status_record = DrinkingFountainStatusRecord(
      is_closed=True,
      start_date='2026-06-01',
      end_date='2026-06-30',
      closed_message=CLOSED_MESSAGE )

   assert DrinkingFountainStatusBuilder.applies_to_date(
      status_record,
      VISIT_DATE ) is True
   assert DrinkingFountainStatusBuilder.applies_to_date(
      status_record,
      OUTSIDE_VISIT_DATE ) is False


def Test_BuildStatus_TestClosedRecord_ExpectZeroLikelihood() -> None:
   status_record = DrinkingFountainStatusRecord(
      is_closed=True,
      start_date='2026-06-01',
      end_date='2026-06-30',
      closed_message=CLOSED_MESSAGE )

   is_closed, closed_message, likelihood = DrinkingFountainStatusBuilder.build_status(
      status_record )

   assert is_closed is True
   assert closed_message == CLOSED_MESSAGE
   assert likelihood == 0.0


def Test_BuildOpenStatus_TestDateRange_ExpectMappedStatus() -> None:
   status = DrinkingFountainStatusBuilder.build_open_status(
      start_date='2026-06-01',
      end_date='2026-06-30' )

   assert status.start_date == '2026-06-01'
   assert status.end_date == '2026-06-30'


def Test_BuildSeasonalStatus_TestLikelihood_ExpectClosedWhenZero() -> None:
   is_closed, closed_message, likelihood = DrinkingFountainStatusBuilder.build_seasonal_status(
      0.0 )

   assert is_closed is True
   assert closed_message is None
   assert likelihood == 0.0


def Test_RecordToModel_TestClosedFountain_ExpectClosedMessageOnlyWhenClosed() -> None:
   fountain = DrinkingFountainBuilder.record_to_model(
      DrinkingFountainRecord( x_coord=1.0, y_coord=2.0 ),
      is_closed=True,
      closed_message=CLOSED_MESSAGE,
      likelihood=0.0 )

   assert fountain.is_closed is True
   assert fountain.closed_message == CLOSED_MESSAGE
