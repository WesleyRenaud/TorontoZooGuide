from __future__ import annotations

from datetime import date

from api.shared.opening_schedule_visit_context import OpeningScheduleVisitContext
from api.transportation.data_access.transportation_record import TransportationRecord
from api.transportation.domain.transportation_builder import TransportationBuilder
from api.transportation.status.transportation_station_status_builder import TransportationStationStatusBuilder


STATION_NAME = 'Africa Zoomobile Station'
WEEKDAY_START_TIME = '10:00 AM'
WEEKDAY_END_TIME = '4:00 PM'
WEEKEND_START_TIME = '11:00 AM'
WEEKEND_END_TIME = '5:00 PM'
WEEKDAY_VISIT_DATE = date( 2026, 6, 15 )
WEEKEND_VISIT_DATE = date( 2026, 6, 20 )
DEFAULT_CLOSED_MESSAGE = 'The Africa Zoomobile Station is temporarily closed.'


def _visit_context( *, target_date: date, is_weekend_or_holiday: bool ) -> OpeningScheduleVisitContext:
   return OpeningScheduleVisitContext(
      normalized_month=target_date.month,
      normalized_day=target_date.day,
      target_date=target_date,
      weekday=target_date.weekday(),
      is_weekend_or_holiday=is_weekend_or_holiday )


def _transportation_record() -> TransportationRecord:
   return TransportationRecord(
      name='Zoomobile',
      is_also_attraction=True,
      free_with_admission=True,
      description='Zoomobile',
      info_link='https://example.com',
      hyperlink_text='Learn more',
      x_coord=1.0,
      y_coord=2.0,
      region='Africa',
      weekday_start_time=WEEKDAY_START_TIME,
      weekday_end_time=WEEKDAY_END_TIME,
      weekend_holiday_start_time=WEEKEND_START_TIME,
      weekend_holiday_end_time=WEEKEND_END_TIME )


def Test_BuildTransportation_TestWeekdayVisit_ExpectWeekdayHours() -> None:
   transportation = TransportationBuilder.build_transportation(
      _transportation_record(),
      _visit_context(
         target_date=WEEKDAY_VISIT_DATE,
         is_weekend_or_holiday=False ) )

   assert transportation.open_time == WEEKDAY_START_TIME
   assert transportation.close_time == WEEKDAY_END_TIME


def Test_BuildTransportation_TestWeekendVisit_ExpectWeekendHours() -> None:
   transportation = TransportationBuilder.build_transportation(
      _transportation_record(),
      _visit_context(
         target_date=WEEKEND_VISIT_DATE,
         is_weekend_or_holiday=True ) )

   assert transportation.open_time == WEEKEND_START_TIME
   assert transportation.close_time == WEEKEND_END_TIME


def Test_BuildTransportationStationClosedStatus_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   status = TransportationStationStatusBuilder.build_transportation_station_closed_status(
      transportation_station=STATION_NAME,
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='' )

   assert status.transportation_station == STATION_NAME
   assert status.message == DEFAULT_CLOSED_MESSAGE
