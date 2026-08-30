from __future__ import annotations

from api.giftshops.status.gift_shop_status_builder import GiftShopStatusBuilder


GIFT_SHOP_NAME = 'Zootique'
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CUSTOM_CLOSED_MESSAGE = 'Closed for maintenance.'
DEFAULT_CLOSED_MESSAGE = 'The Zootique is temporarily closed.'


def Test_BuildClosedSchedule_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   schedule = GiftShopStatusBuilder.build_closed_schedule(
      gift_shop=GIFT_SHOP_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message='' )

   assert schedule.gift_shop == GIFT_SHOP_NAME
   assert schedule.message == DEFAULT_CLOSED_MESSAGE


def Test_BuildClosedSchedule_TestCustomMessage_ExpectMessageRetained() -> None:
   schedule = GiftShopStatusBuilder.build_closed_schedule(
      gift_shop=GIFT_SHOP_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message=CUSTOM_CLOSED_MESSAGE )

   assert schedule.message == CUSTOM_CLOSED_MESSAGE


def Test_BuildOpeningSchedule_TestWeekdayFlags_ExpectMappedSchedule() -> None:
   schedule = GiftShopStatusBuilder.build_opening_schedule(
      gift_shop=GIFT_SHOP_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=True,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=CUSTOM_CLOSED_MESSAGE )

   assert schedule.gift_shop == GIFT_SHOP_NAME
   assert schedule.monday is True
   assert schedule.friday is True


def Test_BuildClosureOverride_TestCustomMessage_ExpectMappedOverride() -> None:
   override = GiftShopStatusBuilder.build_closure_override(
      gift_shop=GIFT_SHOP_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message=CUSTOM_CLOSED_MESSAGE )

   assert override.gift_shop == GIFT_SHOP_NAME
   assert override.is_closed is True
   assert override.message == CUSTOM_CLOSED_MESSAGE
