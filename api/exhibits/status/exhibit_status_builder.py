from __future__ import annotations

from datetime import date

from ...app_strings import AppStringProvider
from ..data_access.exhibit_closure_record import ExhibitClosureRecord
from .exhibit_closed_status import ExhibitClosedStatus
from ...shared.calendar_dates import DateValues
from ...types import DateInput


class ExhibitStatusBuilder():
   @classmethod
   def build_closed_status(
         cls,
         exhibit: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> ExhibitClosedStatus:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      if not message:
         message = AppStringProvider.format( 'guestStatus.locations.temporarilyClosed', name=exhibit )

      return ExhibitClosedStatus(
         exhibit=exhibit,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message )


   @classmethod
   def is_closure_active_on_visit_date(
         cls,
         is_closed: bool,
         closed_start: DateInput,
         closed_end: DateInput,
         target_date: date | None ) -> bool:
      if not is_closed or target_date is None:
         return False

      return DateValues.is_date_in_range(
         target_date=target_date,
         start_date_value=closed_start,
         end_date_value=closed_end )


   @classmethod
   def exhibit_names_closed_on_visit_date(
         cls,
         closure_records: list[ ExhibitClosureRecord ],
         target_date: date ) -> list[ str ]:
      return [
         record.exhibit
         for record in closure_records
         if cls.is_closure_active_on_visit_date(
            True,
            record.closed_start,
            record.closed_end,
            target_date )
      ]
