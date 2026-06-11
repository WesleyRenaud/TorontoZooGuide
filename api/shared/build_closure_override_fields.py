from __future__ import annotations

from .closure_override_fields import ClosureOverrideFields
from .date_values import DateValues
from .strings import SharedStrings
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
      message = SharedStrings.Locations.temporarily_closed( name )

   return ClosureOverrideFields(
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      is_closed=True,
      message=message )
