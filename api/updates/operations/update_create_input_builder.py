from __future__ import annotations

from ..domain.update_type_value_normalizer import UpdateTypeValueNormalizer
from ..inputs.update_create_input import UpdateCreateInput
from ...shared.calendar_dates import DateValues
from ...types import Types


class UpdateCreateInputBuilder():
   @classmethod
   def build(
         cls,
         title: str,
         description: str,
         update_type: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> UpdateCreateInput | None:
      normalized_update_type = UpdateTypeValueNormalizer.normalize( update_type )
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      if not DateValues.is_date_range_ordered(
            start_date_value=date_range.start_date,
            end_date_value=date_range.end_date ):
         return None

      return UpdateCreateInput(
         title=title,
         description=description,
         update_type=normalized_update_type,
         start_date=date_range.start_date,
         end_date=date_range.end_date )
