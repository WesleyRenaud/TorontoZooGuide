from __future__ import annotations

from ..inputs.update_end_input import UpdateEndInput
from ...shared.calendar_dates import DateValues
from ...types import DateInput, DateKey


class UpdateEndInputBuilder():
   @classmethod
   def build(
         cls,
         title: str,
         start_date: DateKey,
         end_date: DateInput ) -> UpdateEndInput:
      if not end_date:
         end_date = DateValues.today_date_key()

      return UpdateEndInput(
         title=title,
         start_date=start_date,
         end_date=end_date )
