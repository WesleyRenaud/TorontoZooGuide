from __future__ import annotations

from datetime import date

from api.app_string_provider import AppStringProvider
from api.drinking_fountains.data_access.drinking_fountain_record import DrinkingFountainRecord
from api.drinking_fountains.data_access.drinking_fountain_status_record import DrinkingFountainStatusRecord
from api.drinking_fountains.domain.drinking_fountain_builder import DrinkingFountainBuilder
from api.drinking_fountains.status.drinking_fountain_status_builder import DrinkingFountainStatusBuilder
from api.shared.enums.position import Position


VISIT_DATE = date( 2026, 6, 15 )
OUTSIDE_VISIT_DATE = date( 2026, 7, 1 )
CLOSED_MESSAGE = 'Closed for testing.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'


def Test_BuildClosedStatus_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   status = DrinkingFountainStatusBuilder.build_closed_status(
      start_date=START_DATE,
      end_date=END_DATE,
      message='' )

   assert status.message == AppStringProvider.format(
      'guestStatus.drinkingFountains.closedForSeason' )


def Test_AppliesToDate_TestVisitDateInRange_ExpectTrue() -> None:
   status_record = DrinkingFountainStatusRecord(
      is_closed=True,
      start_date=START_DATE,
      end_date=END_DATE,
      closed_message=CLOSED_MESSAGE )

   applies = DrinkingFountainStatusBuilder.applies_to_date(
      status_record,
      VISIT_DATE )

   assert applies is True


def Test_AppliesToDate_TestVisitDateOutsideRange_ExpectFalse() -> None:
   status_record = DrinkingFountainStatusRecord(
      is_closed=True,
      start_date=START_DATE,
      end_date=END_DATE,
      closed_message=CLOSED_MESSAGE )

   applies = DrinkingFountainStatusBuilder.applies_to_date(
      status_record,
      OUTSIDE_VISIT_DATE )

   assert applies is False


def Test_BuildStatus_TestClosedRecord_ExpectZeroLikelihood() -> None:
   status_record = DrinkingFountainStatusRecord(
      is_closed=True,
      start_date=START_DATE,
      end_date=END_DATE,
      closed_message=CLOSED_MESSAGE )

   is_closed, closed_message, likelihood = DrinkingFountainStatusBuilder.build_status(
      status_record )

   assert is_closed is True
   assert closed_message == status_record.closed_message
   assert likelihood == 0.0


def Test_BuildOpenStatus_TestDateRange_ExpectMappedStatus() -> None:
   status = DrinkingFountainStatusBuilder.build_open_status(
      start_date=START_DATE,
      end_date=END_DATE )

   assert status.start_date == START_DATE
   assert status.end_date == END_DATE


def Test_BuildSeasonalStatus_TestLikelihood_ExpectClosedWhenZero() -> None:
   seasonal_likelihood = 0.0

   is_closed, closed_message, likelihood = DrinkingFountainStatusBuilder.build_seasonal_status(
      seasonal_likelihood )

   assert is_closed is True
   assert closed_message is None
   assert likelihood == seasonal_likelihood


def Test_RecordToModel_TestClosedFountain_ExpectClosedMessageOnlyWhenClosed() -> None:
   record = DrinkingFountainRecord( x_coord=1.0, y_coord=2.0 )

   fountain = DrinkingFountainBuilder.record_to_model(
      record,
      is_closed=True,
      closed_message=CLOSED_MESSAGE,
      likelihood=0.0 )

   assert fountain.is_closed is True
   assert fountain.closed_message == CLOSED_MESSAGE


def Test_BuildDrinkingFountains_TestRecords_ExpectModels() -> None:
   record = DrinkingFountainRecord( x_coord=1.0, y_coord=2.0 )

   fountains = DrinkingFountainBuilder.build_drinking_fountains(
      [ record ],
      is_closed=True,
      closed_message=CLOSED_MESSAGE,
      likelihood=0.0 )

   assert len( fountains ) == 1
   assert fountains[ Position.FIRST ].is_closed is True
