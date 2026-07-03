from __future__ import annotations

from ...models import Itinerary
from ..scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from ...shared.enums import ItineraryEventType


def itinerary_has_unscheduled_guest_items( itinerary: Itinerary ) -> bool:
   return any(
      not has_itinerary_schedule_times( item.start_time, item.end_time )
      for item in ( *itinerary.animals, *itinerary.attractions )
   ) or any(
      not has_itinerary_schedule_times( event.start_time, event.end_time )
      for event in itinerary.events
      if event.event_type not in (
            ItineraryEventType.ARRIVAL,
            ItineraryEventType.DEPARTURE,
      )
   )


def should_append_return_to_entrance_walk_route_leg(
      itinerary: Itinerary ) -> bool:
   return not itinerary_has_unscheduled_guest_items( itinerary )
