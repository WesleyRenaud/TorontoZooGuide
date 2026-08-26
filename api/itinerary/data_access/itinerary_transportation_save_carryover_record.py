from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryTransportationSaveCarryover:
   name: str
   old_likelihood: int | None
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
   legs: list[ ItineraryTransportationLeg ] = field( default_factory=list )
   bulk_transit_evaluated: bool = False
