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
      *,
      name: str,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      route: str ) -> bool:
   cur.execute(
      """   UPDATE ItineraryTransportation
            SET START_TIME = ?,
                END_TIME = ?,
                ROUTE = ?
            WHERE TRANSPORTATION = ?;
      """,
      (
         DateValues.normalize_itinerary_schedule_time( start_time ),
         DateValues.normalize_itinerary_schedule_time( end_time ),
         route,
         name,
      ),
   )

   return cur.rowcount > 0


def apply_itinerary_transportation_schedule(
      cur: Cursor,
      *,
      name: str,
      start_time: ScheduleTimeKey,
      route: str,
      legs: list[ TransportationRouteLegSegment ] ) -> bool:
   timed_legs, end_time = expand_timed_transportation_legs(
      transportation=name,
      start_time=start_time,
      legs=legs )

   delete_itinerary_transportation_legs( cur, transportation=name )
   insert_itinerary_transportation_legs(
      cur,
      transportation=name,
      legs=timed_legs )

   delete_itinerary_transportation_route_markers( cur, transportation=name )
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
         route_marker_sequences=route_marker_sequences )

   return update_itinerary_transportation_schedule(
      cur,
      name=name,
      start_time=start_time,
      end_time=end_time,
      route=route )
