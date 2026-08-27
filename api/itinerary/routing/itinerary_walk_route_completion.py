from __future__ import annotations

from ...models import Itinerary
from ..scheduling.core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker


def should_append_return_to_entrance_walk_route_leg(
      itinerary: Itinerary ) -> bool:
   return not GuestItemScheduleStatusChecker.has_unscheduled_guest_items( itinerary )
