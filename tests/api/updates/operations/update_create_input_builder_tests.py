from __future__ import annotations

from api.updates.domain.update_type import UpdateType
from api.updates.domain.update_type_value_normalizer import UpdateTypeValueNormalizer
from api.updates.operations.update_create_input_builder import UpdateCreateInputBuilder


UPDATE_TITLE = 'New baby giraffe'
UPDATE_DESCRIPTION = 'Come meet the new calf.'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'


def Test_Normalize_TestDisplayValue_ExpectCanonicalUpdateType() -> None:
   assert UpdateTypeValueNormalizer.normalize( 'New Arrival' ) == UpdateType.NEW_ARRIVAL.value


def Test_Normalize_TestAlias_ExpectCanonicalUpdateType() -> None:
   assert UpdateTypeValueNormalizer.normalize( 'new_arrival' ) == UpdateType.NEW_ARRIVAL.value


def Test_Build_TestValidPayload_ExpectNormalizedCreateInput() -> None:
   create_input = UpdateCreateInputBuilder.build(
      title=UPDATE_TITLE,
      description=UPDATE_DESCRIPTION,
      update_type='New Arrival',
      start_date=START_DATE,
      end_date=END_DATE )

   assert create_input is not None
   assert create_input.title == UPDATE_TITLE
   assert create_input.update_type == UpdateType.NEW_ARRIVAL.value
   assert create_input.start_date == START_DATE
   assert create_input.end_date == END_DATE


def Test_Build_TestInvalidDateRange_ExpectNone() -> None:
   assert UpdateCreateInputBuilder.build(
      title=UPDATE_TITLE,
      description=UPDATE_DESCRIPTION,
      update_type='Closure',
      start_date='2026-06-30',
      end_date='2026-06-01' ) is None
