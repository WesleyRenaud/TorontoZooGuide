from __future__ import annotations

from api.updates.domain.update_type import UpdateType
from api.updates.domain.update_type_value_normalizer import UpdateTypeValueNormalizer
from api.updates.operations.update_create_input_builder import UpdateCreateInputBuilder


UPDATE_TITLE = 'New baby giraffe'
UPDATE_DESCRIPTION = 'Come meet the new calf.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'


def Test_Normalize_TestDisplayValue_ExpectCanonicalUpdateType() -> None:
   value = UpdateType.NEW_ARRIVAL.value

   normalized = UpdateTypeValueNormalizer.normalize( value )

   assert normalized == UpdateType.NEW_ARRIVAL.value


def Test_Normalize_TestAlias_ExpectCanonicalUpdateType() -> None:
   alias = 'new_arrival'

   normalized = UpdateTypeValueNormalizer.normalize( alias )

   assert normalized == UpdateType.NEW_ARRIVAL.value


def Test_Build_TestValidPayload_ExpectNormalizedCreateInput() -> None:
   update_type = UpdateType.NEW_ARRIVAL.value

   create_input = UpdateCreateInputBuilder.build(
      title=UPDATE_TITLE,
      description=UPDATE_DESCRIPTION,
      update_type=update_type,
      start_date=START_DATE,
      end_date=END_DATE )

   assert create_input is not None
   assert create_input.title == UPDATE_TITLE
   assert create_input.update_type == update_type
   assert create_input.start_date == START_DATE
   assert create_input.end_date == END_DATE


def Test_Build_TestInvalidDateRange_ExpectNone() -> None:
   start_date = '2026-06-30'
   end_date = '2026-06-01'

   create_input = UpdateCreateInputBuilder.build(
      title=UPDATE_TITLE,
      description=UPDATE_DESCRIPTION,
      update_type=UpdateType.CLOSURE.value,
      start_date=start_date,
      end_date=end_date )

   assert create_input is None
