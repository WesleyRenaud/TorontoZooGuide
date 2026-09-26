from __future__ import annotations

from api.shared.calendar_dates import DateValues
from api.updates.operations.update_end_input_builder import UpdateEndInputBuilder


def Test_Build_TestMissingEndDate_ExpectToday() -> None:
   title = 'Seasonal closure'
   start_date = '2026-06-01'
   end_date = ''

   result = UpdateEndInputBuilder.build(
      title=title,
      start_date=start_date,
      end_date=end_date )

   assert result.title == title
   assert result.start_date == start_date
   assert result.end_date == DateValues.today_date_key()
