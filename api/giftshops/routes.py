from __future__ import annotations

from .controllers.gift_shop_controller import GiftShopController
from ..json_handler import PostRouteHandler


GIFT_SHOP_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-gift-shops': GiftShopController.get_gift_shops,
   '/get-gift-shop-names': GiftShopController.get_gift_shop_names,
   '/set-gift-shop-closed': GiftShopController.set_gift_shop_closed,
   '/set-gift-shop-closure-override': GiftShopController.set_gift_shop_closure_override,
   '/set-gift-shop-opening-schedule': GiftShopController.set_gift_shop_opening_schedule,
   '/replace-gift-shop-opening-schedule-overlaps': (
      GiftShopController.replace_gift_shop_opening_schedule_overlaps
   ),
   '/trim-gift-shop-opening-schedule-overlaps': (
      GiftShopController.trim_gift_shop_opening_schedule_overlaps
   ),
}
