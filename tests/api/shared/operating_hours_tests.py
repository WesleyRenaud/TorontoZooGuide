from __future__ import annotations

from api.shared.operating_hours import OperatingHours


def Test_FromScheduleTimes_TestValidTimes_ExpectSecondsRange() -> None:
   hours = OperatingHours.from_schedule_times( '10:00 AM', '4:00 PM' )

   assert hours is not None
   assert hours.open_seconds == 10 * 3600
   assert hours.close_seconds == 16 * 3600


def Test_FromScheduleTimes_TestMissingOpenTime_ExpectNone() -> None:
   assert OperatingHours.from_schedule_times( None, '4:00 PM' ) is None
