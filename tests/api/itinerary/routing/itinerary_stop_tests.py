from __future__ import annotations

from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.shared.enums import ScheduleItemKind

def Test_PrimaryWalkNodeId_TestEmptyWalkNodes_ExpectNone() -> None:
   stop = ItineraryStop(
      walk_node_ids=[],
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='African Lion||Africa Savanna' )

   assert stop.primary_walk_node_id() is None
