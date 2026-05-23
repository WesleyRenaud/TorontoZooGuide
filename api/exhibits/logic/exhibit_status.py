from __future__ import annotations

from ...shared.date_values import DateValues
from ...shared.strings import SharedStrings
from ...types import DateInput
from .exhibit_closed_status import ExhibitClosedStatus


def build_exhibit_closed_status(
      exhibit: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> ExhibitClosedStatus:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( exhibit )

   return ExhibitClosedStatus(
      exhibit=exhibit,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
