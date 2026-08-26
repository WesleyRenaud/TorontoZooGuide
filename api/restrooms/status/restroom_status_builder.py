from __future__ import annotations

from ...app_strings import format_app_string
from .restroom_closed_status import RestroomClosedStatus
from ...shared.calendar_dates import DateValues
from ...types import DateInput


class RestroomStatusBuilder():
   @classmethod
   def build_closed_status(
         cls,
         restroom: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> RestroomClosedStatus:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      if not message:
         message = format_app_string( 'guestStatus.locations.temporarilyClosed', name=restroom )

      return RestroomClosedStatus(
         restroom=restroom,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message )
