from __future__ import annotations

from ...itinerary.routing.itinerary_stop import ItineraryStop
from ...itinerary.routing.loop_schedule_pin import LoopSchedulePin
from ...models import GuardiansTalk
from ...shared.calendar_dates import DateValues
from ...walk_graph.domain.master_route_loop import MasterRouteLoop
from ...walk_graph.master_route import default_master_route_loop_by_id


def resolve_guardians_talk_loop_pin(
      guardians_talk: GuardiansTalk,
      itinerary_stop: ItineraryStop ) -> LoopSchedulePin | None:
   start_seconds = DateValues.time_value_in_seconds( itinerary_stop.start_time )
   end_seconds = DateValues.time_value_in_seconds( itinerary_stop.end_time )

   if start_seconds is None or end_seconds is None:
      return None

   loops_by_id = default_master_route_loop_by_id()

   for loop_id, master_route_loop in loops_by_id.items():
      viewing_spot_index = viewing_spot_index_for_talk_in_loop(
         master_route_loop,
         talk_name=guardians_talk.name,
         talk_location=guardians_talk.location )

      if viewing_spot_index is not None:
         return LoopSchedulePin(
            loop_id=loop_id,
            viewing_spot_index=viewing_spot_index,
            stop=itinerary_stop,
            start_seconds=start_seconds,
            end_seconds=end_seconds )

   return None


def viewing_spot_index_for_talk_in_loop(
      master_route_loop: MasterRouteLoop,
      *,
      talk_name: str,
      talk_location: str ) -> int | None:
   for index, viewing_spot in enumerate( master_route_loop.viewing_spots ):
      if (
            viewing_spot.species == talk_name
            and viewing_spot.exhibit == talk_location ):
         return index

   return None
