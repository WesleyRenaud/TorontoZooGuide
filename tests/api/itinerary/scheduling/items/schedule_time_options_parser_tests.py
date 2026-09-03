from __future__ import annotations

from api.itinerary.scheduling.items.parsed_schedule_time_options import ParsedScheduleTimeOptions
from api.itinerary.scheduling.items.schedule_time_options_parser import ScheduleTimeOptionsParser
from api.shared.enums import ItineraryErrorType


def Test_Parse_TestDurationWithoutTime_ExpectParsedOptions() -> None:
   assert ScheduleTimeOptionsParser.parse( None, 30 ) == ParsedScheduleTimeOptions(
      start_time=None,
      duration_minutes=30,
   )
   assert ScheduleTimeOptionsParser.parse( '   ', 30 ) == ParsedScheduleTimeOptions(
      start_time=None,
      duration_minutes=30,
   )


def Test_Parse_TestInvalidStartTime_ExpectSaveFailed() -> None:
   assert ScheduleTimeOptionsParser.parse( 'not-a-time', None ) == ItineraryErrorType.SAVE_FAILED


def Test_Parse_TestInvalidDuration_ExpectSaveFailed() -> None:
   assert ScheduleTimeOptionsParser.parse(
      '10:00 AM',
      0,
   ) == ItineraryErrorType.SAVE_FAILED
