from __future__ import annotations

from api.restaurants.status.restaurant_status_builder import RestaurantStatusBuilder


RESTAURANT_NAME = 'Africa Restaurant'
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CUSTOM_CLOSED_MESSAGE = 'Closed for maintenance.'
DEFAULT_CLOSED_MESSAGE = 'The Africa Restaurant is temporarily closed.'


def Test_BuildClosedSchedule_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   schedule = RestaurantStatusBuilder.build_closed_schedule(
      restaurant=RESTAURANT_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message='' )

   assert schedule.restaurant == RESTAURANT_NAME
   assert schedule.message == DEFAULT_CLOSED_MESSAGE


def Test_BuildClosedSchedule_TestCustomMessage_ExpectMessageRetained() -> None:
   schedule = RestaurantStatusBuilder.build_closed_schedule(
      restaurant=RESTAURANT_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message=CUSTOM_CLOSED_MESSAGE )

   assert schedule.message == CUSTOM_CLOSED_MESSAGE


def Test_BuildOpeningSchedule_TestWeekdayFlags_ExpectMappedSchedule() -> None:
   schedule = RestaurantStatusBuilder.build_opening_schedule(
      restaurant=RESTAURANT_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      monday=True,
      tuesday=False,
      wednesday=True,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=CUSTOM_CLOSED_MESSAGE )

   assert schedule.restaurant == RESTAURANT_NAME
   assert schedule.monday is True
   assert schedule.wednesday is True


def Test_BuildClosureOverride_TestCustomMessage_ExpectMappedOverride() -> None:
   override = RestaurantStatusBuilder.build_closure_override(
      restaurant=RESTAURANT_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message=CUSTOM_CLOSED_MESSAGE )

   assert override.restaurant == RESTAURANT_NAME
   assert override.is_closed is True
   assert override.message == CUSTOM_CLOSED_MESSAGE
