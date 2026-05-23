from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class GiftShopScheduleOverrideRecord:
   gift_shop: str
   override_start_date: DateKey
   override_end_date: DateKey | None
   is_closed: bool
   override_message: str | None
