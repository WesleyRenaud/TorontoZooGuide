from __future__ import annotations

from datetime import date

from api.attractions.data_access.attraction_record import AttractionRecord
from api.attractions.data_access.attraction_schedule_override_record import AttractionScheduleOverrideRecord
from api.attractions.data_access.attraction_schedule_record import AttractionScheduleRecord
from api.attractions.domain.attraction_builder import AttractionBuilder
from api.shared.enums.schedule_status import ScheduleStatus
from api.shared.opening_schedule_visit_context import OpeningScheduleVisitContext


ATTRACTION_NAME = 'Conservation Carousel'
TRANSPORTATION_ATTRACTION_NAME = 'Zoomobile'
WEEKDAY_START_TIME = '10:00 AM'
WEEKDAY_END_TIME = '4:00 PM'
WEEKEND_START_TIME = '11:00 AM'
WEEKEND_END_TIME = '5:00 PM'
CUSTOM_SCHEDULE_MESSAGE = 'Closed for testing.'
WEEKENDS_ONLY_MESSAGE = (
   'The Conservation Carousel is open on weekends and holidays only.'
)
NOT_SCHEDULED_MESSAGE = (
   'The Conservation Carousel is not scheduled to be open today.'
)
WEEKDAY_VISIT_DATE = date( 2026, 6, 15 )
WEEKEND_VISIT_DATE = date( 2026, 6, 20 )
OVERRIDE_START_DATE = date( 2026, 6, 20 )
OPEN_AFTER_OVERRIDE_DATE = date( 2026, 6, 22 )
CLOSURE_OVERRIDE_MESSAGE = 'Closed this weekend.'


def _visit_context( *, target_date: date, is_weekend_or_holiday: bool ) -> OpeningScheduleVisitContext:
   return OpeningScheduleVisitContext(
      normalized_month=target_date.month,
      normalized_day=target_date.day,
      target_date=target_date,
      weekday=target_date.weekday(),
      is_weekend_or_holiday=is_weekend_or_holiday )


def _attraction_record( **overrides: object ) -> AttractionRecord:
   values: dict[ str, object ] = {
      'name': ATTRACTION_NAME,
      'free_with_admission': True,
      'description': 'Carousel',
      'info_link': 'https://example.com',
      'hyperlink_text': 'Learn more',
      'x_coord': 1.0,
      'y_coord': 2.0,
      'region': 'Front Courtyard',
      'weekday_multiplier': 1.0,
      'weekend_holiday_multiplier': 1.0,
      'weekday_start_time': WEEKDAY_START_TIME,
      'weekday_end_time': WEEKDAY_END_TIME,
      'weekend_holiday_start_time': WEEKEND_START_TIME,
      'weekend_holiday_end_time': WEEKEND_END_TIME,
      'is_also_transportation': False,
   }
   values.update( overrides )

   return AttractionRecord( **values )


def _schedule_record( **overrides: object ) -> AttractionScheduleRecord:
   values: dict[ str, object ] = {
      'attraction': ATTRACTION_NAME,
      'schedule_start_date': '2026-06-01',
      'schedule_end_date': '2026-06-30',
      'monday': True,
      'tuesday': True,
      'wednesday': True,
      'thursday': True,
      'friday': True,
      'saturday': True,
      'sunday': True,
      'holidays_only': False,
      'schedule_message': None,
   }
   values.update( overrides )

   return AttractionScheduleRecord( **values )


def _override_record( **overrides: object ) -> AttractionScheduleOverrideRecord:
   values: dict[ str, object ] = {
      'attraction': ATTRACTION_NAME,
      'override_start_date': '2026-06-20',
      'override_end_date': '2026-06-21',
      'is_closed': True,
      'override_message': CLOSURE_OVERRIDE_MESSAGE,
   }
   values.update( overrides )

   return AttractionScheduleOverrideRecord( **values )


def Test_CalculateLikelihood_TestSeasonalMultiplier_ExpectClampedAndRounded() -> None:
   assert AttractionBuilder.calculate_likelihood( None ) == 100
   assert AttractionBuilder.calculate_likelihood( -0.5 ) == 0
   assert AttractionBuilder.calculate_likelihood( 0.444 ) == 44
   assert AttractionBuilder.calculate_likelihood( 1.5 ) == 100


def Test_BuildClosedScheduleMessage_TestCustomMessage_ExpectScheduleMessageRetained() -> None:
   schedule_record = _schedule_record( schedule_message=CUSTOM_SCHEDULE_MESSAGE )

   assert AttractionBuilder.build_closed_schedule_message(
      ATTRACTION_NAME,
      schedule_record ) == CUSTOM_SCHEDULE_MESSAGE


def Test_BuildClosedScheduleMessage_TestWeekendsAndHolidaysOnly_ExpectDefaultMessage() -> None:
   schedule_record = _schedule_record(
      saturday=True,
      sunday=True,
      holidays_only=True )

   assert AttractionBuilder.build_closed_schedule_message(
      ATTRACTION_NAME,
      schedule_record ) == WEEKENDS_ONLY_MESSAGE


def Test_BuildClosedScheduleMessage_TestNoCustomMessage_ExpectNotScheduledTodayMessage() -> None:
   schedule_record = _schedule_record()

   assert AttractionBuilder.build_closed_schedule_message(
      ATTRACTION_NAME,
      schedule_record ) == NOT_SCHEDULED_MESSAGE


def Test_BuildAttraction_TestWeekdayVisit_ExpectWeekdayHours() -> None:
   attraction = AttractionBuilder.build_attraction(
      attraction_record=_attraction_record(),
      schedule_records=[],
      schedule_override_records=[],
      context=_visit_context(
         target_date=WEEKDAY_VISIT_DATE,
         is_weekend_or_holiday=False ) )

   assert attraction.open_time == WEEKDAY_START_TIME
   assert attraction.close_time == WEEKDAY_END_TIME
   assert attraction.likelihood == 100
   assert attraction.is_closed is False


def Test_BuildAttraction_TestWeekendVisit_ExpectWeekendHours() -> None:
   attraction = AttractionBuilder.build_attraction(
      attraction_record=_attraction_record(),
      schedule_records=[],
      schedule_override_records=[],
      context=_visit_context(
         target_date=WEEKEND_VISIT_DATE,
         is_weekend_or_holiday=True ) )

   assert attraction.open_time == WEEKEND_START_TIME
   assert attraction.close_time == WEEKEND_END_TIME


def Test_BuildAttraction_TestTransportationFlag_ExpectIsAlsoTransportationRetained() -> None:
   attraction = AttractionBuilder.build_attraction(
      attraction_record=_attraction_record(
         name=TRANSPORTATION_ATTRACTION_NAME,
         is_also_transportation=True ),
      schedule_records=[],
      schedule_override_records=[],
      context=_visit_context(
         target_date=WEEKDAY_VISIT_DATE,
         is_weekend_or_holiday=False ) )

   assert attraction.is_also_transportation is True
   assert attraction.to_dict()[ 'is_also_transportation' ] is True


def Test_BuildAttractions_TestClosedAttraction_ExpectExcludedUnlessRequested() -> None:
   closed_attraction_record = _attraction_record(
      weekday_multiplier=0,
      weekend_holiday_multiplier=0 )
   context = _visit_context(
      target_date=WEEKDAY_VISIT_DATE,
      is_weekend_or_holiday=False )

   open_only = AttractionBuilder.build_attractions(
      attraction_records=[ closed_attraction_record ],
      schedule_records=[],
      schedule_override_records=[],
      context=context,
      include_closed_attractions=False )
   with_closed = AttractionBuilder.build_attractions(
      attraction_records=[ closed_attraction_record ],
      schedule_records=[],
      schedule_override_records=[],
      context=context,
      include_closed_attractions=True )

   assert open_only == []
   assert len( with_closed ) == 1
   assert with_closed[ 0 ].is_closed is True


def Test_GetActiveScheduleStatus_TestOpenMonday_ExpectOpen() -> None:
   status, message = AttractionBuilder.get_active_schedule_status(
      schedule_records=[ _schedule_record( monday=True ) ],
      attraction_name=ATTRACTION_NAME,
      target_date=WEEKDAY_VISIT_DATE,
      weekday=WEEKDAY_VISIT_DATE.weekday() )

   assert status == ScheduleStatus.OPEN
   assert message is None


def Test_BuildAttraction_TestClosureOverrideOnClosedDay_ExpectOverrideMessage() -> None:
   attraction = AttractionBuilder.build_attraction(
      attraction_record=_attraction_record(),
      schedule_records=[ _schedule_record() ],
      schedule_override_records=[ _override_record() ],
      context=_visit_context(
         target_date=OVERRIDE_START_DATE,
         is_weekend_or_holiday=True ) )

   assert attraction.is_closed is True
   assert attraction.closed_message == CLOSURE_OVERRIDE_MESSAGE


def Test_BuildAttraction_TestClosureOverrideOutsideRange_ExpectOpenFromSchedule() -> None:
   attraction = AttractionBuilder.build_attraction(
      attraction_record=_attraction_record(),
      schedule_records=[ _schedule_record() ],
      schedule_override_records=[ _override_record() ],
      context=_visit_context(
         target_date=OPEN_AFTER_OVERRIDE_DATE,
         is_weekend_or_holiday=False ) )

   assert attraction.is_closed is False
   assert attraction.closed_message is None
