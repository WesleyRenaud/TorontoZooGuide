from __future__ import annotations

from ..domain.update_type_value_normalizer import UpdateTypeValueNormalizer
from ..inputs.update_edit_input import UpdateEditInput
from ...shared.calendar_dates import DateValues
from ...types import DateInput, DateKey


class UpdateEditInputBuilder():
   @classmethod
   def build(
         cls,
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
         update_type=UpdateTypeValueNormalizer.normalize( update_type ),
         end_date=normalized_end_date )
