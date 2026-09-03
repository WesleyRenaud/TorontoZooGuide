from __future__ import annotations

from datetime import date

from api.giftshops.data_access.gift_shop_record import GiftShopRecord
from api.giftshops.data_access.gift_shop_schedule_override_record import GiftShopScheduleOverrideRecord
from api.giftshops.data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from api.giftshops.domain.gift_shop_builder import GiftShopBuilder
from api.shared.enums.schedule_status import ScheduleStatus
from api.shared.opening_schedule_visit_context import OpeningScheduleVisitContext


GIFT_SHOP_NAME = 'Zootique'
CUSTOM_CLOSED_MESSAGE = 'Closed for testing.'
CLOSURE_OVERRIDE_MESSAGE = 'Closed this weekend.'
VISIT_DATE = date( 2026, 6, 15 )
OVERRIDE_VISIT_DATE = date( 2026, 6, 20 )
OPEN_AFTER_OVERRIDE_DATE = date( 2026, 6, 22 )


def _visit_context_for( target_date: date, *, is_weekend_or_holiday: bool = False ) -> OpeningScheduleVisitContext:
   return OpeningScheduleVisitContext(
      normalized_month=target_date.month,
      normalized_day=target_date.day,
      target_date=target_date,
      weekday=target_date.weekday(),
      is_weekend_or_holiday=is_weekend_or_holiday )


def _visit_context() -> OpeningScheduleVisitContext:
   return _visit_context_for( VISIT_DATE )


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


def _override_record( **overrides: object ) -> GiftShopScheduleOverrideRecord:
   values: dict[ str, object ] = {
      'gift_shop': GIFT_SHOP_NAME,
      'override_start_date': '2026-06-20',
      'override_end_date': '2026-06-21',
      'is_closed': True,
      'override_message': CLOSURE_OVERRIDE_MESSAGE,
   }
   values.update( overrides )

   return GiftShopScheduleOverrideRecord( **values )


def Test_CalculateLikelihood_TestSeasonalMultiplier_ExpectClampedAndRounded() -> None:
   assert GiftShopBuilder.calculate_likelihood( None ) == 100
   assert GiftShopBuilder.calculate_likelihood( -0.5 ) == 0
   assert GiftShopBuilder.calculate_likelihood( 0.444 ) == 44
   assert GiftShopBuilder.calculate_likelihood( 1.5 ) == 100


def Test_GetActiveScheduleStatus_TestOpenMonday_ExpectOpen() -> None:
   status, message = GiftShopBuilder.get_active_schedule_status(
      schedule_records=[ _schedule_record( monday=True ) ],
      target_date=VISIT_DATE,
      weekday=VISIT_DATE.weekday() )

   assert status == ScheduleStatus.OPEN
   assert message is None


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


def Test_BuildGiftShop_TestClosureOverrideOnClosedDay_ExpectOverrideMessage() -> None:
   gift_shop = GiftShopBuilder.build_gift_shop(
      gift_shop_record=_gift_shop_record(),
      schedule_records=[ _schedule_record(
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ) ],
      schedule_override_records=[ _override_record() ],
      context=_visit_context_for(
         OVERRIDE_VISIT_DATE,
         is_weekend_or_holiday=True ) )

   assert gift_shop.is_closed is True
   assert gift_shop.closed_message == CLOSURE_OVERRIDE_MESSAGE


def Test_BuildGiftShop_TestClosureOverrideOutsideRange_ExpectOpenFromSchedule() -> None:
   gift_shop = GiftShopBuilder.build_gift_shop(
      gift_shop_record=_gift_shop_record(),
      schedule_records=[ _schedule_record(
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ) ],
      schedule_override_records=[ _override_record() ],
      context=_visit_context_for( OPEN_AFTER_OVERRIDE_DATE ) )

   assert gift_shop.is_closed is False
   assert gift_shop.closed_message is None


def Test_ResolveContext_TestVisitDay_ExpectVisitContext() -> None:
   context = GiftShopBuilder.resolve_context( day=15, month='June', year=2026 )

   assert context.normalized_day == 15
   assert context.normalized_month == 6


def Test_IsOpenOnDay_TestMondaySchedule_ExpectOpenOnMonday() -> None:
   schedule = _schedule_record( monday=True )

   assert GiftShopBuilder.is_open_on_day(
      schedule,
      weekday=VISIT_DATE.weekday(),
      is_holiday=False ) is True


def Test_GetActiveScheduleOverrideStatus_TestClosedOverride_ExpectClosed() -> None:
   status, message = GiftShopBuilder.get_active_schedule_override_status(
      override_records=[ _override_record() ],
      target_date=OVERRIDE_VISIT_DATE )

   assert status == ScheduleStatus.CLOSED
   assert message == CLOSURE_OVERRIDE_MESSAGE
