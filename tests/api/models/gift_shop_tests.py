from __future__ import annotations

from api.models.gift_shop import GiftShop


def Test_ToDict_TestClosedFlag_ExpectFrontendShape() -> None:
   assert GiftShop( name='Shop', location='Gate', is_closed=0 ).to_dict()[ 'is_closed' ] is False
