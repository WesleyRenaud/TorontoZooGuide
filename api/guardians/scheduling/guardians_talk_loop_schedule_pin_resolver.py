from __future__ import annotations

from ...guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from .guardians_talk_loop_viewing_spot_index_resolver import GuardiansTalkLoopViewingSpotIndexResolver
from ...itinerary.routing.itinerary_stop import ItineraryStop
from ...itinerary.routing.loop_schedule_pin import LoopSchedulePin
from ...models import GuardiansTalk
from ...shared.calendar_dates import DateValues
from ...types import Types
from ...walk_graph.master_route_provider import MasterRouteProvider


class GuardiansTalkLoopSchedulePinResolver():
   @classmethod
   def resolve(
         cls,
         conn: Types.Connection,
         guardians_talk: GuardiansTalk,
         itinerary_stop: ItineraryStop ) -> LoopSchedulePin | None:
      start_seconds = DateValues.time_value_in_seconds( itinerary_stop.start_time )
      end_seconds = DateValues.time_value_in_seconds( itinerary_stop.end_time )

      if start_seconds is None or end_seconds is None:
         return None

      linked_animals = GuardiansTalkAnimalProvider.fetch_animal_links(
         conn,
         guardians_talk.name )
      loops_by_id = MasterRouteProvider.loops_by_id()

      for loop_id, master_route_loop in loops_by_id.items():
         viewing_spot_index = GuardiansTalkLoopViewingSpotIndexResolver.resolve(
            master_route_loop,
            talk_name=guardians_talk.name,
            talk_location=guardians_talk.location,
            linked_animals=linked_animals )

         if viewing_spot_index is not None:
            return LoopSchedulePin(
               loop_id=loop_id,
               viewing_spot_index=viewing_spot_index,
               stop=itinerary_stop,
               start_seconds=start_seconds,
               end_seconds=end_seconds )

      return None
