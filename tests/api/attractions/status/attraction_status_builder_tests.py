from __future__ import annotations

from api.app_string_provider import AppStringProvider
from api.attractions.status.attraction_status_builder import AttractionStatusBuilder


ATTRACTION_NAME = 'Conservation Carousel'
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CUSTOM_CLOSED_MESSAGE = 'Closed for maintenance.'


def Test_BuildClosedSchedule_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   schedule = AttractionStatusBuilder.build_closed_schedule(
      attraction=ATTRACTION_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message='' )

   assert schedule.attraction == ATTRACTION_NAME
   assert schedule.start_date == CLOSURE_START_DATE
   assert schedule.end_date == CLOSURE_END_DATE
   assert schedule.message == AppStringProvider.format(
      'guestStatus.locations.temporarilyClosed',
      name=ATTRACTION_NAME )


def Test_BuildClosedSchedule_TestCustomMessage_ExpectMessageRetained() -> None:
   schedule = AttractionStatusBuilder.build_closed_schedule(
      attraction=ATTRACTION_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message=CUSTOM_CLOSED_MESSAGE )

   assert schedule.message == CUSTOM_CLOSED_MESSAGE


def Test_BuildOpeningSchedule_TestWeekdayFlags_ExpectMappedSchedule() -> None:
   monday = True
   wednesday = True

   schedule = AttractionStatusBuilder.build_opening_schedule(
      attraction=ATTRACTION_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      monday=monday,
      tuesday=False,
      wednesday=wednesday,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=CUSTOM_CLOSED_MESSAGE )

   assert schedule.attraction == ATTRACTION_NAME
   assert schedule.monday is monday
   assert schedule.wednesday is wednesday
   assert schedule.message == CUSTOM_CLOSED_MESSAGE


def Test_BuildClosureOverride_TestCustomMessage_ExpectMappedOverride() -> None:
   override = AttractionStatusBuilder.build_closure_override(
      attraction=ATTRACTION_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message=CUSTOM_CLOSED_MESSAGE )

   assert override.attraction == ATTRACTION_NAME
   assert override.is_closed is True
   assert override.message == CUSTOM_CLOSED_MESSAGE
