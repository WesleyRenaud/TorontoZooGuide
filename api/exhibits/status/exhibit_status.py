from __future__ import annotations

from ...app_strings import format_app_string
from .exhibit_closed_status import ExhibitClosedStatus
from ...shared.calendar_dates import DateValues
from ...types import DateInput


def build_exhibit_closed_status(
      exhibit: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> ExhibitClosedStatus:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = format_app_string( 'guestStatus.locations.temporarilyClosed', name=exhibit )

   return ExhibitClosedStatus(
      exhibit=exhibit,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
