from __future__ import annotations

from api.models.gift_shop import GiftShop
from api.shared.value_conversion import ValueConversion


def Test_ToDict_TestClosedFlag_ExpectFrontendShape() -> None:
   gift_shop = GiftShop( name='Shop', location='Gate', is_closed=0 )

   result = gift_shop.to_dict()

   assert result[ 'is_closed' ] is ValueConversion.as_boolean( gift_shop.is_closed )
