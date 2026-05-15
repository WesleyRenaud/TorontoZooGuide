from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class GiftShopContext:
   normalized_month: int
   normalized_day: int
   target_date: date
   weekday: int
   is_weekend_or_holiday: bool
