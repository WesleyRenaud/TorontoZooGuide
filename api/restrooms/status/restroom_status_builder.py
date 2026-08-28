from __future__ import annotations

from ...app_string_provider import AppStringProvider
from .restroom_closed_status import RestroomClosedStatus
from ...shared.calendar_dates import DateValues
from ...types import Types


class RestroomStatusBuilder():
   @classmethod
   def build_closed_status(
         cls,
         restroom: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> RestroomClosedStatus:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      if not message:
         message = AppStringProvider.format( 'guestStatus.locations.temporarilyClosed', name=restroom )

      return RestroomClosedStatus(
         restroom=restroom,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message )
