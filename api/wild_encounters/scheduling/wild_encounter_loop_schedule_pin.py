from __future__ import annotations

from ..data_access.wild_encounter_meeting_spot_loop_pin_record import WildEncounterMeetingSpotLoopPinRecord
from ...itinerary.routing.itinerary_stop import ItineraryStop
from ...itinerary.routing.loop_schedule_pin import LoopSchedulePin
from ...models import WildEncounter
from ...shared.calendar_dates import DateValues
from ...walk_graph.master_route_provider import MasterRouteProvider


def resolve_wild_encounter_loop_pin(
      wild_encounter: WildEncounter,
      itinerary_stop: ItineraryStop,
      *,
      meeting_spot_loop_pins_by_name: dict[
         str,
         WildEncounterMeetingSpotLoopPinRecord ],
   ) -> LoopSchedulePin | None:
   meeting_spot_loop_pin = meeting_spot_loop_pins_by_name.get(
      wild_encounter.meeting_spot )

   if meeting_spot_loop_pin is None:
      return None

   start_seconds = DateValues.time_value_in_seconds( itinerary_stop.start_time )
   end_seconds = DateValues.time_value_in_seconds( itinerary_stop.end_time )

   if start_seconds is None or end_seconds is None:
      return None

   if MasterRouteProvider.loops_by_id().get( meeting_spot_loop_pin.loop_id ) is None:
      return None

   return LoopSchedulePin(
      loop_id=meeting_spot_loop_pin.loop_id,
      viewing_spot_index=meeting_spot_loop_pin.loop_viewing_spot_index,
      stop=itinerary_stop,
      start_seconds=start_seconds,
      end_seconds=end_seconds )
