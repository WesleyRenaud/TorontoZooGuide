from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class AttractionHoursClock:
   weekday_start_time: Types.TimeInput
   weekday_end_time: Types.TimeInput
   weekend_holiday_start_time: Types.TimeInput
   weekend_holiday_end_time: Types.TimeInput
