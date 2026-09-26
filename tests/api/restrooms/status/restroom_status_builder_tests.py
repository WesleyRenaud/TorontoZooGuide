from __future__ import annotations

from api.app_string_provider import AppStringProvider
from api.restrooms.status.restroom_alert_builder import RestroomAlertBuilder
from api.restrooms.status.restroom_status_builder import RestroomStatusBuilder


RESTROOM_NAME = 'Entrance Restroom'
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
ALERT_START_DATE = '2026-06-01'
ALERT_END_DATE = '2026-06-30'
ALERT_MESSAGE = "Women's restroom is temporarily unavailable."


def Test_BuildClosedStatus_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   status = RestroomStatusBuilder.build_closed_status(
      restroom=RESTROOM_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message='' )

   assert status.restroom == RESTROOM_NAME
   assert status.message == AppStringProvider.format(
      'guestStatus.locations.temporarilyClosed',
      name=RESTROOM_NAME )


def Test_BuildAlert_TestExplicitDates_ExpectAlertFieldsRetained() -> None:
   alert = RestroomAlertBuilder.build_alert(
      restroom=RESTROOM_NAME,
      alert_start_date=ALERT_START_DATE,
      alert_end_date=ALERT_END_DATE,
      message=ALERT_MESSAGE )

   assert alert.restroom == RESTROOM_NAME
   assert alert.start_date == ALERT_START_DATE
   assert alert.end_date == ALERT_END_DATE
   assert alert.message == ALERT_MESSAGE
