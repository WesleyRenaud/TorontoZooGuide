from __future__ import annotations

from datetime import date

from api.giftshops.data_access.gift_shop_closure_record import GiftShopClosureRecord
from api.giftshops.domain.seasonal_gift_shop import SeasonalGiftShop
from api.giftshops.domain.seasonal_gift_shop_builder import SeasonalGiftShopBuilder


ZOOTIQUE = 'Zootique'


def Test_Build_TestClosures_ExpectGiftShopNameStatusAndDates() -> None:
   gift_shops = SeasonalGiftShopBuilder.build(
      gift_shops=[ ZOOTIQUE, 'Kangaroo Shop' ],
      closure_records=[
         GiftShopClosureRecord(
            gift_shop=ZOOTIQUE,
            closed_start='2026-11-02',
            closed_end='2026-11-30',
            closed_message=None,
            is_closed_for_season=True,
         ),
         GiftShopClosureRecord(
            gift_shop='Missing Start',
            closed_start=None,
            closed_end=None,
            closed_message=None,
            is_closed_for_season=True,
         ),
         GiftShopClosureRecord(
            gift_shop='Gorilla Shop',
            closed_start='2026-10-01',
            closed_end=None,
            closed_message=None,
            is_closed_for_season=True,
         ),
      ],
   )

   assert gift_shops == [
      SeasonalGiftShop(
         name=ZOOTIQUE,
         is_closed=True,
         start=date( 2026, 11, 2 ),
         end=date( 2026, 11, 30 ),
         closed_for_season=True,
      ),
      SeasonalGiftShop(
         name='Kangaroo Shop',
         is_closed=False,
         start=None,
         end=None,
         closed_for_season=False,
      ),
      SeasonalGiftShop(
         name='Gorilla Shop',
         is_closed=True,
         start=date( 2026, 10, 1 ),
         end=None,
         closed_for_season=True,
      ),
   ]


def Test_ClosedForSeasonOn_TestOpenEndedRange_ExpectOnlyCoveredDate() -> None:
   gift_shop = SeasonalGiftShop(
      name=ZOOTIQUE,
      is_closed=True,
      start=date( 2026, 11, 2 ),
      end=None,
      closed_for_season=True,
   )

   assert gift_shop.closed_for_season_on( date( 2026, 11, 2 ) )
   assert not gift_shop.closed_for_season_on( date( 2026, 11, 1 ) )
