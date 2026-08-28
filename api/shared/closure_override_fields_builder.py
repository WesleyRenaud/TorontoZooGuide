from __future__ import annotations

from ..app_strings import AppStringProvider
from .calendar_dates import DateValues
from .closure_override_fields import ClosureOverrideFields
from ..types import DateInput


class ClosureOverrideFieldsBuilder():
   @classmethod
   def build(
         cls,
         name: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> ClosureOverrideFields:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      if not message:
         message = AppStringProvider.format( 'guestStatus.locations.temporarilyClosed', name=name )

      return ClosureOverrideFields(
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         is_closed=True,
         message=message )
