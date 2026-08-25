from __future__ import annotations

from .restroom_alert import RestroomAlert
from ...shared.calendar_dates import DateValues
from ...types import DateInput


class RestroomAlertBuilder():
   @classmethod
   def build_alert(
         cls,
         restroom: str,
         alert_start_date: DateInput,
         alert_end_date: DateInput,
         message: str ) -> RestroomAlert:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=alert_start_date,
         end_date=alert_end_date )

      return RestroomAlert(
         restroom=restroom,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message )
