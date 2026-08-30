from __future__ import annotations

from datetime import date

from api.attractions.data_access.attraction_record import AttractionRecord
from api.attractions.scheduling.attraction_operating_hours_resolver import AttractionOperatingHoursResolver
from api.shared.operating_hours import OperatingHours


WEEKDAY_VISIT_DATE = date( 2026, 6, 15 )
WEEKEND_VISIT_DATE = date( 2026, 6, 20 )
WEEKDAY_START_TIME = '10:00 AM'
WEEKDAY_END_TIME = '4:00 PM'
WEEKEND_START_TIME = '11:00 AM'
WEEKEND_END_TIME = '5:00 PM'
ZOO_OPEN_SECONDS = 9 * 3600
ZOO_CLOSE_SECONDS = 18 * 3600


def _attraction_record() -> AttractionRecord:
   return AttractionRecord(
      name='Conservation Carousel',
      free_with_admission=True,
      description='Carousel',
      info_link='https://example.com',
      hyperlink_text='Learn more',
      x_coord=1.0,
      y_coord=2.0,
      region='Americas',
      weekday_multiplier=1.0,
      weekend_holiday_multiplier=1.0,
      weekday_start_time=WEEKDAY_START_TIME,
      weekday_end_time=WEEKDAY_END_TIME,
      weekend_holiday_start_time=WEEKEND_START_TIME,
      weekend_holiday_end_time=WEEKEND_END_TIME )


def Test_HasConfiguredOperatingHours_TestWeekdayTimes_ExpectTrue() -> None:
   assert AttractionOperatingHoursResolver.has_configured_operating_hours(
      _attraction_record(),
      visit_date=WEEKDAY_VISIT_DATE )


def Test_OperatingHoursSeconds_TestWeekdayVisit_ExpectConfiguredHours() -> None:
   zoo_hours = OperatingHours(
      open_seconds=ZOO_OPEN_SECONDS,
      close_seconds=ZOO_CLOSE_SECONDS )

   hours = AttractionOperatingHoursResolver.operating_hours_seconds(
      _attraction_record(),
      visit_date=WEEKDAY_VISIT_DATE,
      zoo_operating_hours=zoo_hours )

   assert hours.open_seconds == 10 * 3600
   assert hours.close_seconds == 16 * 3600


def Test_OperatingHoursSeconds_TestWeekendVisit_ExpectWeekendConfiguredHours() -> None:
   zoo_hours = OperatingHours(
      open_seconds=ZOO_OPEN_SECONDS,
      close_seconds=ZOO_CLOSE_SECONDS )

   hours = AttractionOperatingHoursResolver.operating_hours_seconds(
      _attraction_record(),
      visit_date=WEEKEND_VISIT_DATE,
      zoo_operating_hours=zoo_hours )

   assert hours.open_seconds == 11 * 3600
   assert hours.close_seconds == 17 * 3600


def Test_OperatingHoursSeconds_TestMissingAttractionTimes_ExpectZooFallback() -> None:
   attraction_record = AttractionRecord(
      name='Conservation Carousel',
      free_with_admission=True,
      description='Carousel',
      info_link='https://example.com',
      hyperlink_text='Learn more',
      x_coord=1.0,
      y_coord=2.0,
      region='Americas',
      weekday_multiplier=1.0,
      weekend_holiday_multiplier=1.0 )
   zoo_hours = OperatingHours(
      open_seconds=ZOO_OPEN_SECONDS,
      close_seconds=ZOO_CLOSE_SECONDS )

   hours = AttractionOperatingHoursResolver.operating_hours_seconds(
      attraction_record,
      visit_date=WEEKDAY_VISIT_DATE,
      zoo_operating_hours=zoo_hours )

   assert hours.open_seconds == ZOO_OPEN_SECONDS
   assert hours.close_seconds == ZOO_CLOSE_SECONDS
