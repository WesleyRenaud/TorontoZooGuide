from __future__ import annotations

from ..domain.transportation_route_marker_sequences_builder import TransportationRouteMarkerSequencesBuilder
from .itinerary_transportation_provider import ItineraryTransportationProvider
from .itinerary_transportation_route_marker_provider import ItineraryTransportationRouteMarkerProvider
from ...shared.calendar_dates import DateValues
from ..transportation.timed_transportation_leg_expander import TimedTransportationLegExpander
from ..transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from ...types import Types


class ScheduleItineraryTransportationProvider():
   @classmethod
   def update_itinerary_transportation_schedule(
         cls,
         cur: Types.Cursor,
         name: str,
         added_as_attraction: bool,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey,
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


   @classmethod
   def apply_itinerary_transportation_schedule(
         cls,
         cur: Types.Cursor,
         name: str,
         added_as_attraction: bool,
         start_time: Types.ScheduleTimeKey,
         route: str,
         legs: list[ TransportationRouteLegSegment ] ) -> bool:
      return cls.apply_itinerary_transportation_ride_segments(
         cur,
         name=name,
         added_as_attraction=added_as_attraction,
         route=route,
         segments=[ ( start_time, legs ) ] )


   @classmethod
   def apply_itinerary_transportation_ride_segments(
         cls,
         cur: Types.Cursor,
         name: str,
         added_as_attraction: bool,
         route: str,
         segments: list[ tuple[ Types.ScheduleTimeKey, list[ TransportationRouteLegSegment ] ] ],
   ) -> bool:
      if not segments:
         return False

      timed_legs: list = []
      parent_start_time = segments[ 0 ][ 0 ]
      parent_end_time = segments[ 0 ][ 0 ]

      for start_time, legs in segments:
         if not legs:
            continue

         segment_legs, end_time = TimedTransportationLegExpander.expand(
            transportation=name,
            start_time=start_time,
            legs=legs,
            added_as_attraction=added_as_attraction )
         timed_legs.extend( segment_legs )
         parent_end_time = end_time

      if not timed_legs:
         return False

      ItineraryTransportationProvider.delete_itinerary_transportation_legs(
         cur,
         transportation=name,
         added_as_attraction=added_as_attraction )
      ItineraryTransportationProvider.insert_itinerary_transportation_legs(
         cur,
         transportation=name,
         added_as_attraction=added_as_attraction,
         legs=timed_legs )

      ItineraryTransportationRouteMarkerProvider.delete_itinerary_transportation_route_markers(
         cur,
         transportation=name,
         added_as_attraction=added_as_attraction )
      route_marker_sequences = TransportationRouteMarkerSequencesBuilder.build(
         cur.connection,
         transportation=name,
         route=route,
         legs=timed_legs,
      )

      if route_marker_sequences:
         ItineraryTransportationRouteMarkerProvider.insert_itinerary_transportation_route_markers(
            cur,
            transportation=name,
            added_as_attraction=added_as_attraction,
            route_marker_sequences=route_marker_sequences )

      return cls.update_itinerary_transportation_schedule(
         cur,
         name=name,
         added_as_attraction=added_as_attraction,
         start_time=parent_start_time,
         end_time=parent_end_time,
         route=route )
