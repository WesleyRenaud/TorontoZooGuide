from __future__ import annotations

from api.itinerary.scheduling.items.parsed_schedule_time_options import ParsedScheduleTimeOptions

def Test_ToDict_TestStartTimeAndDuration_ExpectDictionary() -> None:
   options = ParsedScheduleTimeOptions(
      start_time='10:00 AM',
      duration_minutes=30 )

   assert options.to_dict() == {
      'start_time': '10:00 AM',
      'duration_minutes': 30,
   }
