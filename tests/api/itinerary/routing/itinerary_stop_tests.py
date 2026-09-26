from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.shared.enums import ScheduleItemKind


def Test_PrimaryWalkNodeId_TestEmptyWalkNodes_ExpectNone() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   stop = ItineraryStop(
      walk_node_ids=[],
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key=AnimalScheduleItemKey.wire( species=species, exhibit=exhibit ) )

   walk_node_id = stop.primary_walk_node_id()

   assert walk_node_id is None
