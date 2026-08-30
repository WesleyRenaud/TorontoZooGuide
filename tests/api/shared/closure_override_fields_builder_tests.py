from __future__ import annotations

from api.shared.closure_override_fields_builder import ClosureOverrideFieldsBuilder


LOCATION_NAME = 'Africa Restaurant'
START_DATE = '2026-06-01'
END_DATE = '2026-06-07'
CUSTOM_MESSAGE = 'Closed for a private event.'


def Test_Build_TestCustomMessage_ExpectClosedOverrideFields() -> None:
   fields = ClosureOverrideFieldsBuilder.build(
      name=LOCATION_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CUSTOM_MESSAGE )

   assert fields.start_date == START_DATE
   assert fields.end_date == END_DATE
   assert fields.is_closed is True
   assert fields.message == CUSTOM_MESSAGE


def Test_Build_TestMissingMessage_ExpectDefaultClosedMessage() -> None:
   fields = ClosureOverrideFieldsBuilder.build(
      name=LOCATION_NAME,
      start_date=START_DATE,
      end_date=None,
      message='' )

   assert fields.end_date is None
   assert LOCATION_NAME in fields.message
