from __future__ import annotations

from datetime import date

from ..data_access.exhibit_closure_record import ExhibitClosureRecord
from ...shared.date_values import DateValues
from ...types import DateInput


def is_exhibit_closure_active_on_visit_date(
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


def exhibit_names_closed_on_visit_date(
      closure_records: list[ ExhibitClosureRecord ],
      target_date: date ) -> list[ str ]:
   return [
      record.exhibit
      for record in closure_records
      if is_exhibit_closure_active_on_visit_date(
         True,
         record.closed_start,
         record.closed_end,
         target_date )
   ]
