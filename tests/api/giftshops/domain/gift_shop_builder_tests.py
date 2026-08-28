from __future__ import annotations

from datetime import date

from api.giftshops.data_access.gift_shop_record import GiftShopRecord
from api.giftshops.data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from api.giftshops.domain.gift_shop_builder import GiftShopBuilder
from api.shared.opening_schedule_visit_context import OpeningScheduleVisitContext


GIFT_SHOP_NAME = 'Zootique'
CUSTOM_CLOSED_MESSAGE = 'Closed for testing.'
VISIT_DATE = date( 2026, 6, 15 )


def _visit_context() -> OpeningScheduleVisitContext:
   return OpeningScheduleVisitContext(
      normalized_month=VISIT_DATE.month,
      normalized_day=VISIT_DATE.day,
      target_date=VISIT_DATE,
      weekday=VISIT_DATE.weekday(),
      is_weekend_or_holiday=False )


def _gift_shop_record( **overrides: object ) -> GiftShopRecord:
   values: dict[ str, object ] = {
      'name': GIFT_SHOP_NAME,
      'location': 'Africa',
      'description': 'Gift shop',
      'x_coord': 1.0,
      'y_coord': 2.0,
      'weekday_multiplier': 1.0,
      'weekend_holiday_multiplier': 1.0,
   }
   values.update( overrides )

   return GiftShopRecord( **values )


def _schedule_record( **overrides: object ) -> GiftShopScheduleRecord:
   values: dict[ str, object ] = {
      'gift_shop': GIFT_SHOP_NAME,
      'schedule_start_date': '2026-06-01',
      'schedule_end_date': '2026-06-30',
      'monday': False,
      'tuesday': False,
      'wednesday': False,
      'thursday': False,
      'friday': False,
      'saturday': False,
      'sunday': False,
      'holidays_only': False,
      'schedule_message': CUSTOM_CLOSED_MESSAGE,
   }
   values.update( overrides )

   return GiftShopScheduleRecord( **values )


def Test_CalculateLikelihood_TestSeasonalMultiplier_ExpectClampedAndRounded() -> None:
   assert GiftShopBuilder.calculate_likelihood( None ) == 100
   assert GiftShopBuilder.calculate_likelihood( -0.5 ) == 0
   assert GiftShopBuilder.calculate_likelihood( 0.444 ) == 44
   assert GiftShopBuilder.calculate_likelihood( 1.5 ) == 100


def Test_BuildGiftShops_TestClosedGiftShop_ExpectExcludedUnlessIncludedOrListed() -> None:
   context = _visit_context()
   closed_record = _gift_shop_record( weekday_multiplier=0, weekend_holiday_multiplier=0 )
   schedule_records = [ _schedule_record() ]

   open_only = GiftShopBuilder.build_gift_shops(
      gift_shop_records=[ closed_record ],
      schedule_records=schedule_records,
      schedule_override_records=[],
      context=context,
      include_closed_gift_shops=False )
   with_closed = GiftShopBuilder.build_gift_shops(
      gift_shop_records=[ closed_record ],
      schedule_records=schedule_records,
      schedule_override_records=[],
      context=context,
      include_closed_gift_shops=True )
   explicitly_listed = GiftShopBuilder.build_gift_shops(
      gift_shop_records=[ closed_record ],
      schedule_records=schedule_records,
      schedule_override_records=[],
      context=context,
      include_closed_gift_shops=False,
      gift_shops_to_include=[ GIFT_SHOP_NAME ] )

   assert open_only == []
   assert len( with_closed ) == 1
   assert with_closed[ 0 ].is_closed is True
   assert len( explicitly_listed ) == 1


def Test_BuildGiftShop_TestClosedSchedule_ExpectCustomClosedMessage() -> None:
   gift_shop = GiftShopBuilder.build_gift_shop(
      gift_shop_record=_gift_shop_record(),
      schedule_records=[ _schedule_record() ],
      schedule_override_records=[],
      context=_visit_context() )

   assert gift_shop.is_closed is True
   assert gift_shop.closed_message == CUSTOM_CLOSED_MESSAGE
