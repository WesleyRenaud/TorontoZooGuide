from __future__ import annotations

from api.restaurants.scheduling.restaurant_opening_schedule import RestaurantOpeningSchedule
from api.restaurants.scheduling.restaurant_schedule_override import RestaurantScheduleOverride
from api.shared.amenity_status_builders import AmenityStatusBuilders
from api.shared.enums.amenity_name_field import AmenityNameField


RESTAURANT_NAME = 'Africa Restaurant'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
CUSTOM_MESSAGE = 'Closed for a private event.'

BUILDERS = AmenityStatusBuilders(
   name_field=AmenityNameField.RESTAURANT,
   opening_schedule_class=RestaurantOpeningSchedule,
   schedule_override_class=RestaurantScheduleOverride,
)


def Test_BuildClosedSchedule_TestCustomMessage_ExpectRestaurantOpeningSchedule() -> None:
   schedule = BUILDERS.build_closed_schedule(
      RESTAURANT_NAME,
      START_DATE,
      END_DATE,
      CUSTOM_MESSAGE )

   assert schedule.restaurant == RESTAURANT_NAME
   assert schedule.start_date == START_DATE
   assert schedule.end_date == END_DATE
   assert schedule.monday is False
   assert schedule.sunday is False
   assert schedule.message == CUSTOM_MESSAGE


def Test_BuildOpeningSchedule_TestWeekdayFlags_ExpectRestaurantOpeningSchedule() -> None:
   schedule = BUILDERS.build_opening_schedule(
      RESTAURANT_NAME,
      START_DATE,
      END_DATE,
      monday=True,
      tuesday=False,
      wednesday=True,
      thursday=False,
      friday=True,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=CUSTOM_MESSAGE )

   assert schedule.restaurant == RESTAURANT_NAME
   assert schedule.monday is True
   assert schedule.wednesday is True
   assert schedule.friday is True
   assert schedule.message == CUSTOM_MESSAGE


def Test_BuildClosureOverride_TestCustomMessage_ExpectRestaurantScheduleOverride() -> None:
   override = BUILDERS.build_closure_override(
      RESTAURANT_NAME,
      START_DATE,
      END_DATE,
      CUSTOM_MESSAGE )

   assert override.restaurant == RESTAURANT_NAME
   assert override.start_date == START_DATE
   assert override.end_date == END_DATE
   assert override.is_closed is True
   assert override.message == CUSTOM_MESSAGE
