from __future__ import annotations

from api.restrooms.status.restroom_alert_builder import RestroomAlertBuilder
from api.restrooms.status.restroom_status_builder import RestroomStatusBuilder


RESTROOM_NAME = 'Entrance Restroom'
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
ALERT_START_DATE = '2026-06-01'
ALERT_END_DATE = '2026-06-30'
CUSTOM_CLOSED_MESSAGE = 'Closed for maintenance.'
DEFAULT_CLOSED_MESSAGE = 'The Entrance Restroom is temporarily closed.'
ALERT_MESSAGE = "Women's restroom is temporarily unavailable."


def Test_BuildClosedStatus_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   status = RestroomStatusBuilder.build_closed_status(
      restroom=RESTROOM_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message='' )

   assert status.restroom == RESTROOM_NAME
   assert status.message == DEFAULT_CLOSED_MESSAGE


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
