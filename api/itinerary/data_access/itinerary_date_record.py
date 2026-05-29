from __future__ import annotations

from dataclasses import dataclass

from ...types import DateInput, ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryDateRecord:
   itinerary_date: DateInput
   arrival_time: ScheduleTimeKey
   departure_time: ScheduleTimeKey
