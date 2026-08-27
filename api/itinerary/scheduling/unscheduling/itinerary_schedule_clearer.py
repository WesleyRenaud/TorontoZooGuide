from __future__ import annotations

from ...data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from ...data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from ....types import Connection
from ....types import Cursor


class ItineraryScheduleClearer():
   @classmethod
   def _clear_guest_items( cls, cur: Cursor ) -> None:
      UnscheduleItineraryItemProvider.clear_all_itinerary_animal_schedules( cur )
      UnscheduleItineraryItemProvider.clear_all_itinerary_attraction_schedules( cur )
      UnscheduleItineraryItemProvider.clear_all_itinerary_transportation_schedules( cur )
      UnscheduleItineraryItemProvider.clear_all_scheduled_itinerary_events( cur )


   @classmethod
   def clear_guest_items( cls, conn: Connection ) -> None:
      cur = conn.cursor()

      try:
         cls._clear_guest_items( cur )
         conn.commit()

      finally:
         cur.close()


   @classmethod
   def clear_all( cls, conn: Connection ) -> None:
      cur = conn.cursor()

      try:
         cls._clear_guest_items( cur )
         ItineraryWalkRouteProvider.clear_itinerary_walk_route( cur )
         conn.commit()

      finally:
         cur.close()
