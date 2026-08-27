from __future__ import annotations

from ...models import Itinerary
from ..scheduling.core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker


class ItineraryWalkRouteCompletionChecker():
   @classmethod
   def should_append_return_to_entrance_leg( cls, itinerary: Itinerary ) -> bool:
      return not GuestItemScheduleStatusChecker.has_unscheduled_guest_items(
         itinerary )
