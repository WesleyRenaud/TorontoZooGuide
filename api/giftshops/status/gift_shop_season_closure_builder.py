from __future__ import annotations

from datetime import date

from ...app_string_provider import AppStringProvider
from ..data_access.gift_shop_closure_record import GiftShopClosureRecord
from .gift_shop_season_closure import GiftShopSeasonClosure
from ...shared.calendar_dates import DateValues
from ...types import Types


class GiftShopSeasonClosureBuilder():
   @classmethod
   def build(
         cls,
         gift_shop: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> GiftShopSeasonClosure:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      if not message:
         message = AppStringProvider.format(
            'guestStatus.locations.closedForSeason',
            name=gift_shop )

      return GiftShopSeasonClosure(
         gift_shop=gift_shop,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message,
         is_closed_for_season=True )


   @classmethod
   def is_active_on_date(
         cls,
         closure_record: GiftShopClosureRecord | None,
         target_date: date | None ) -> bool:
      if closure_record == None or target_date == None:
         return False

      return DateValues.is_date_in_range(
         target_date=target_date,
         start_date_value=closure_record.closed_start,
         end_date_value=closure_record.closed_end )
