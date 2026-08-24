from __future__ import annotations

from ..domain.build_transportation_route_marker_sequences import build_transportation_route_marker_sequences
from .itinerary_transportation import delete_itinerary_transportation_legs
from .itinerary_transportation import insert_itinerary_transportation_legs
from .itinerary_transportation_route_markers import delete_itinerary_transportation_route_markers
from .itinerary_transportation_route_markers import insert_itinerary_transportation_route_markers
from ...shared.calendar_dates import DateValues
from ..transportation.expand_timed_transportation_legs import expand_timed_transportation_legs
from ..transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from ...types import Cursor
from ...types import ScheduleTimeKey


def update_itinerary_transportation_schedule(
      cur: Cursor,
      name: str,
      added_as_attraction: bool,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      route: str ) -> bool:
   cur.execute(
      """   UPDATE ItineraryTransportation
            SET START_TIME = ?,
                END_TIME = ?,
                ROUTE = ?
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = ?;
      """,
      (
         DateValues.normalize_itinerary_schedule_time( start_time ),
         DateValues.normalize_itinerary_schedule_time( end_time ),
         route,
         name,
         added_as_attraction,
      ),
   )

   return cur.rowcount > 0


def apply_itinerary_transportation_schedule(
      cur: Cursor,
      name: str,
      added_as_attraction: bool,
      start_time: ScheduleTimeKey,
      route: str,
      legs: list[ TransportationRouteLegSegment ] ) -> bool:
   return apply_itinerary_transportation_ride_segments(
      cur,
      name=name,
      added_as_attraction=added_as_attraction,
      route=route,
      segments=[ ( start_time, legs ) ] )


def apply_itinerary_transportation_ride_segments(
      cur: Cursor,
      name: str,
      added_as_attraction: bool,
      route: str,
      segments: list[ tuple[ ScheduleTimeKey, list[ TransportationRouteLegSegment ] ] ],
) -> bool:
   if not segments:
      return False

   timed_legs: list = []
   parent_start_time = segments[ 0 ][ 0 ]
   parent_end_time = segments[ 0 ][ 0 ]

   for start_time, legs in segments:
      if not legs:
         continue

      segment_legs, end_time = expand_timed_transportation_legs(
         transportation=name,
         start_time=start_time,
         legs=legs,
         added_as_attraction=added_as_attraction )
      timed_legs.extend( segment_legs )
      parent_end_time = end_time

   if not timed_legs:
      return False

   delete_itinerary_transportation_legs(
      cur,
      transportation=name,
      added_as_attraction=added_as_attraction )
   insert_itinerary_transportation_legs(
      cur,
      transportation=name,
      added_as_attraction=added_as_attraction,
      legs=timed_legs )

   delete_itinerary_transportation_route_markers(
      cur,
      transportation=name,
      added_as_attraction=added_as_attraction )
   route_marker_sequences = build_transportation_route_marker_sequences(
      cur.connection,
      transportation=name,
      route=route,
      legs=timed_legs,
   )

   if route_marker_sequences:
      insert_itinerary_transportation_route_markers(
         cur,
         transportation=name,
         added_as_attraction=added_as_attraction,
         route_marker_sequences=route_marker_sequences )

   return update_itinerary_transportation_schedule(
      cur,
      name=name,
      added_as_attraction=added_as_attraction,
      start_time=parent_start_time,
      end_time=parent_end_time,
      route=route )
