from __future__ import annotations

from api.shared.calendar_dates import DateValues
from api.shared.operating_hours import OperatingHours


def Test_FromScheduleTimes_TestValidTimes_ExpectSecondsRange() -> None:
   open_time = '10:00 AM'
   close_time = '4:00 PM'

   hours = OperatingHours.from_schedule_times( open_time, close_time )

   assert hours is not None
   assert hours.open_seconds == DateValues.time_value_in_seconds( open_time )
   assert hours.close_seconds == DateValues.time_value_in_seconds( close_time )


def Test_FromScheduleTimes_TestMissingOpenTime_ExpectNone() -> None:
   open_time = None
   close_time = '4:00 PM'

   hours = OperatingHours.from_schedule_times( open_time, close_time )

   assert hours is None
