from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class ItineraryDateRecord:
   itinerary_date: Types.DateInput
   arrival_time: Types.ScheduleTimeKey
   departure_time: Types.ScheduleTimeKey
