from __future__ import annotations

from api.attractions.scheduling.attraction_hours_seen_days import AttractionHoursSeenDays
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


def Test_Add_TestMissingOperatingDate_ExpectNone() -> None:
   seen = AttractionHoursSeenDays()
   day = seen.add( ZooHoursRecord(
      operating_date=None,
      early_admission_time='9:00 AM',
      open_time='9:30 AM',
      last_admission_time='6:00 PM',
      close_time='7:00 PM',
   ) )

   assert day is None
   assert not seen.both_day_kinds()
