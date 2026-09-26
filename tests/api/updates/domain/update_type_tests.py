from __future__ import annotations

from api.updates.domain.update_type import UpdateType
from api.updates.domain.update_type_display_order_resolver import UpdateTypeDisplayOrderResolver
from api.updates.domain.update_type_value_normalizer import UpdateTypeValueNormalizer


def Test_Normalize_TestCanonicalValue_ExpectSameType() -> None:
   value = UpdateType.CLOSURE.value

   update_type = UpdateType.normalize( value )

   assert update_type is UpdateType.CLOSURE


def Test_Normalize_TestAlias_ExpectMappedType() -> None:
   value = 'animal_birth'

   update_type = UpdateType.normalize( value )

   assert update_type is UpdateType.ANIMAL_BIRTH


def Test_Normalize_TestUnknownValue_ExpectNone() -> None:
   value = 'Unknown Type'

   update_type = UpdateType.normalize( value )

   assert update_type is None


def Test_Normalize_TestNone_ExpectNone() -> None:
   value = None

   update_type = UpdateType.normalize( value )

   assert update_type is None


def Test_DisplayOrder_TestKnownTypes_ExpectConfiguredOrder() -> None:
   update_types = list( UpdateType )

   orders = [ update_type.order for update_type in update_types ]

   assert orders == list( range( len( update_types ) ) )


def Test_ValueNormalizer_TestAlias_ExpectCanonicalValue() -> None:
   alias = 'new_arrival'

   value = UpdateTypeValueNormalizer.normalize( alias )

   assert value == UpdateType.NEW_ARRIVAL.value


def Test_DisplayOrderResolver_TestKnownType_ExpectConfiguredOrder() -> None:
   update_type = UpdateType.CLOSURE.value

   order = UpdateTypeDisplayOrderResolver.resolve( update_type )

   assert order == UpdateType.CLOSURE.order


def Test_DisplayOrderResolver_TestUnknownType_ExpectSortsAfterKnownTypes() -> None:
   update_type = 'Unknown Type'

   order = UpdateTypeDisplayOrderResolver.resolve( update_type )

   assert order == len( UpdateType )
