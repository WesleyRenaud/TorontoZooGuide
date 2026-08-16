from __future__ import annotations

from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.calendar_dates import DateValues
from ...shared.duration_values import duration_minutes_to_seconds
from .transportation_route_leg_segment import TransportationRouteLegSegment
from ...types import ScheduleTimeKey


def expand_timed_transportation_legs(
      *,
      start_time: ScheduleTimeKey,
      legs: list[ TransportationRouteLegSegment ],
) -> tuple[ list[ ItineraryTransportationLeg ], ScheduleTimeKey ]:
   start_seconds = DateValues.time_value_in_seconds( start_time )

   if start_seconds is None:
      raise ValueError( 'start_time is required to expand transportation legs' )

   cursor_seconds = start_seconds
   end_time_key: ScheduleTimeKey = start_time
   timed_legs: list[ ItineraryTransportationLeg ] = []

   for leg in legs:
      leg_start_time = DateValues.schedule_time_key_from_seconds( cursor_seconds )
      cursor_seconds += duration_minutes_to_seconds( leg.duration_minutes )
      leg_end_time = DateValues.schedule_time_key_from_seconds( cursor_seconds )
      end_time_key = leg_end_time
      timed_legs.append(
         ItineraryTransportationLeg(
            from_station=leg.from_station,
            to_station=leg.to_station,
            start_time=leg_start_time,
            end_time=leg_end_time ) )

   return timed_legs, end_time_key
