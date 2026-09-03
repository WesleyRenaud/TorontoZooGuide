from __future__ import annotations

from api.updates.operations.update_end_input_builder import UpdateEndInputBuilder

def Test_Build_TestMissingEndDate_ExpectToday() -> None:
   result = UpdateEndInputBuilder.build(
      title='Seasonal closure',
      start_date='2026-06-01',
      end_date='' )

   assert result.title == 'Seasonal closure'
   assert result.start_date == '2026-06-01'
   assert result.end_date is not None
