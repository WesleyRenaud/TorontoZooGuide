from __future__ import annotations

from ...types import DateKey


class GiftShopScheduleOverride:
   def __init__(
         self,
         gift_shop: str,
         start_date: DateKey,
         end_date: DateKey | None,
         is_closed: bool,
         message: str | None ) -> None:
      self.gift_shop = gift_shop
      self.start_date = start_date
      self.end_date = end_date
      self.is_closed = is_closed
      self.message = message
