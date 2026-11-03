from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class GiftShopClosureRecord:
   gift_shop: str
   closed_start: Types.DateKey
   closed_end: Types.DateKey | None
   closed_message: str | None
   is_closed_for_season: bool
