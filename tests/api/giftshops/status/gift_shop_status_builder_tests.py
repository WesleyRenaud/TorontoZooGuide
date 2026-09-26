from __future__ import annotations

from api.app_string_provider import AppStringProvider
from api.giftshops.status.gift_shop_status_builder import GiftShopStatusBuilder


GIFT_SHOP_NAME = 'Zootique'
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CUSTOM_CLOSED_MESSAGE = 'Closed for maintenance.'


def Test_BuildClosedSchedule_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   schedule = GiftShopStatusBuilder.build_closed_schedule(
      gift_shop=GIFT_SHOP_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message='' )

   assert schedule.gift_shop == GIFT_SHOP_NAME
   assert schedule.message == AppStringProvider.format(
      'guestStatus.locations.temporarilyClosed',
      name=GIFT_SHOP_NAME )


def Test_BuildClosedSchedule_TestCustomMessage_ExpectMessageRetained() -> None:
   schedule = GiftShopStatusBuilder.build_closed_schedule(
      gift_shop=GIFT_SHOP_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message=CUSTOM_CLOSED_MESSAGE )

   assert schedule.message == CUSTOM_CLOSED_MESSAGE


def Test_BuildOpeningSchedule_TestWeekdayFlags_ExpectMappedSchedule() -> None:
   monday = True
   friday = True

   schedule = GiftShopStatusBuilder.build_opening_schedule(
      gift_shop=GIFT_SHOP_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      monday=monday,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=friday,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=CUSTOM_CLOSED_MESSAGE )

   assert schedule.gift_shop == GIFT_SHOP_NAME
   assert schedule.monday is monday
   assert schedule.friday is friday


def Test_BuildClosureOverride_TestCustomMessage_ExpectMappedOverride() -> None:
   schedule = GiftShopStatusBuilder.build_closure_override(
      gift_shop=GIFT_SHOP_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message=CUSTOM_CLOSED_MESSAGE )

   assert schedule.gift_shop == GIFT_SHOP_NAME
   assert schedule.is_closed is True
   assert schedule.message == CUSTOM_CLOSED_MESSAGE
