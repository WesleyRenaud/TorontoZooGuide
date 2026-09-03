from __future__ import annotations

from api.updates.domain.update_type_value_normalizer import UpdateTypeValueNormalizer

def Test_Normalize_TestUnknownType_ExpectNone() -> None:
   assert UpdateTypeValueNormalizer.normalize( 'not-a-real-update-type' ) is None

def Test_Normalize_TestKnownType_ExpectValue() -> None:
   assert UpdateTypeValueNormalizer.normalize( 'closure' ) == 'Closure'
