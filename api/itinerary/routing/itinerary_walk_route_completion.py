from __future__ import annotations

from ...models import Itinerary
from ..scheduling.core.guest_item_schedule_status import itinerary_has_unscheduled_guest_items


def should_append_return_to_entrance_walk_route_leg(
      itinerary: Itinerary ) -> bool:
   return not itinerary_has_unscheduled_guest_items( itinerary )
