from __future__ import annotations

from typing import Any

from api.models.gift_shop import GiftShop


class StubGiftShopCoordinator():
   instances: list[ StubGiftShopCoordinator ] = []
   default_success: bool = True


   def __init__(
         self,
         *,
         gift_shop_names: list[ str ],
         gift_shops: list[ GiftShop ] ) -> None:
      self.gift_shop_names = gift_shop_names
      self.gift_shops = gift_shops
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubGiftShopCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_gift_shop_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_gift_shop_names', {} ) )
      return list( self.gift_shop_names )


   def get_gift_shops(
         self,
         *,
         day: int,
         month: str,
         year: int,
         include_closed_gift_shops: bool | None = None,
         gift_shops_to_include: list[ str ] | None = None ) -> list[ GiftShop ]:
      self.calls.append(
         (
            'get_gift_shops',
            {
               'day': day,
               'month': month,
               'year': year,
               'include_closed_gift_shops': include_closed_gift_shops,
               'gift_shops_to_include': gift_shops_to_include,
            }
         )
      )
      return list( self.gift_shops )


   def set_gift_shop_as_closed( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_gift_shop_as_closed', kwargs ) )
      return StubGiftShopCoordinator.default_success


   def set_gift_shop_closure_override( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_gift_shop_closure_override', kwargs ) )
      return StubGiftShopCoordinator.default_success


   def set_gift_shop_opening_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_gift_shop_opening_schedule', kwargs ) )
      return StubGiftShopCoordinator.default_success


   def replace_gift_shop_opening_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'replace_gift_shop_opening_schedule_overlaps', kwargs ) )
      return StubGiftShopCoordinator.default_success


   def trim_gift_shop_opening_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'trim_gift_shop_opening_schedule_overlaps', kwargs ) )
      return StubGiftShopCoordinator.default_success
