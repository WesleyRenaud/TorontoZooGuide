from __future__ import annotations

from ...shared.calendar_dates import DateValues
from ...types import DateInput, DateKey
from .update_edit_input import UpdateEditInput
from .update_type import normalize_update_type


def build_update_edit_input(
      title: str,
      start_date: DateKey,
      description: str,
      update_type: str,
      end_date: DateInput ) -> UpdateEditInput:
   normalized_end_date = None

   if end_date != None:
      normalized_end_date = DateValues.normalize_date_key( end_date )

   return UpdateEditInput(
      title=title,
      start_date=start_date,
      description=description,
      update_type=normalize_update_type( update_type ),
      end_date=normalized_end_date )
