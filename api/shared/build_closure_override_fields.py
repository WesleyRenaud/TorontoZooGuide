from __future__ import annotations

from ..app_strings import format_app_string
from .calendar_dates import DateValues
from .closure_override_fields import ClosureOverrideFields
from ..types import DateInput


def build_closure_override_fields(
      name: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> ClosureOverrideFields:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = format_app_string( 'guestStatus.locations.temporarilyClosed', name=name )

   return ClosureOverrideFields(
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      is_closed=True,
      message=message )
