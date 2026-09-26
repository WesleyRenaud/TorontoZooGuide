from __future__ import annotations

from api.updates.domain.update_type import UpdateType
from api.updates.domain.update_type_value_normalizer import UpdateTypeValueNormalizer


def Test_Normalize_TestUnknownType_ExpectNone() -> None:
   update_type = 'not-a-real-update-type'

   normalized = UpdateTypeValueNormalizer.normalize( update_type )

   assert normalized is None


def Test_Normalize_TestKnownType_ExpectValue() -> None:
   update_type = 'closure'

   normalized = UpdateTypeValueNormalizer.normalize( update_type )

   assert normalized == UpdateType.CLOSURE.value
