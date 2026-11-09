from __future__ import annotations

from ...types import Types


class GiftShopSeasonClosure:
   gift_shop: str
   start_date: Types.DateKey
   end_date: Types.DateKey | None
   message: str
   is_closed_for_season: bool


   def __init__(
         self,
         gift_shop: str,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None,
         message: str,
         is_closed_for_season: bool ) -> None:
      self.gift_shop = gift_shop
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
      self.is_closed_for_season = is_closed_for_season
