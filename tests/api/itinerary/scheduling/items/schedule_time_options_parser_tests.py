from __future__ import annotations

from api.itinerary.scheduling.items.parsed_schedule_time_options import ParsedScheduleTimeOptions
from api.itinerary.scheduling.items.schedule_time_options_parser import ScheduleTimeOptionsParser
from api.shared.enums import ItineraryErrorType


def Test_Parse_TestMissingStartTime_ExpectDurationOnly() -> None:
   duration_minutes = 30

   options = ScheduleTimeOptionsParser.parse( None, duration_minutes )

   assert options == ParsedScheduleTimeOptions(
      start_time=None,
      duration_minutes=duration_minutes )


def Test_Parse_TestBlankStartTime_ExpectDurationOnly() -> None:
   duration_minutes = 30

   options = ScheduleTimeOptionsParser.parse( '   ', duration_minutes )

   assert options == ParsedScheduleTimeOptions(
      start_time=None,
      duration_minutes=duration_minutes )


def Test_Parse_TestInvalidStartTime_ExpectSaveFailed() -> None:
   options = ScheduleTimeOptionsParser.parse( 'not-a-time', None )

   assert options == ItineraryErrorType.SAVE_FAILED


def Test_Parse_TestInvalidDuration_ExpectSaveFailed() -> None:
   start_time = '10:00 AM'
   duration_minutes = 0

   options = ScheduleTimeOptionsParser.parse( start_time, duration_minutes )

   assert options == ItineraryErrorType.SAVE_FAILED
