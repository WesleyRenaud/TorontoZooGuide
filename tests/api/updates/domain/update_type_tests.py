from __future__ import annotations

from api.updates.domain.update_type import UpdateType
from api.updates.domain.update_type_display_order_resolver import UpdateTypeDisplayOrderResolver
from api.updates.domain.update_type_value_normalizer import UpdateTypeValueNormalizer


def Test_Normalize_TestCanonicalValue_ExpectSameType() -> None:
   assert UpdateType.normalize( 'Closure' ) == UpdateType.CLOSURE


def Test_Normalize_TestAlias_ExpectMappedType() -> None:
   assert UpdateType.normalize( 'animal_birth' ) == UpdateType.ANIMAL_BIRTH


def Test_Normalize_TestUnknownValue_ExpectNone() -> None:
   assert UpdateType.normalize( 'Unknown Type' ) is None


def Test_DisplayOrder_TestKnownTypes_ExpectConfiguredOrder() -> None:
   assert UpdateType.CLOSURE.order == 0
   assert UpdateType.ANIMAL_BIRTH.order == 1
   assert UpdateType.ANIMAL_PASSING.order == 2
   assert UpdateType.NEW_ARRIVAL.order == 3
   assert UpdateType.DEPARTURE.order == 4


def Test_ValueNormalizer_TestAlias_ExpectCanonicalValue() -> None:
   assert UpdateTypeValueNormalizer.normalize( 'new_arrival' ) == 'New Arrival'


def Test_DisplayOrderResolver_TestKnownType_ExpectConfiguredOrder() -> None:
   assert UpdateTypeDisplayOrderResolver.resolve( 'Closure' ) == 0


def Test_DisplayOrderResolver_TestUnknownType_ExpectSortsAfterKnownTypes() -> None:
   assert UpdateTypeDisplayOrderResolver.resolve( 'Unknown Type' ) == len( UpdateType )
