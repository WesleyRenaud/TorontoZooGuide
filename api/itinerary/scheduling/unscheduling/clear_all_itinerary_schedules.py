from __future__ import annotations

from ...data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from ...data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from ....types import Connection
from ....types import Cursor


def _clear_guest_scheduled_item_schedules( cur: Cursor ) -> None:
   UnscheduleItineraryItemProvider.clear_all_itinerary_animal_schedules( cur )
   UnscheduleItineraryItemProvider.clear_all_itinerary_attraction_schedules( cur )
   UnscheduleItineraryItemProvider.clear_all_itinerary_transportation_schedules( cur )
   UnscheduleItineraryItemProvider.clear_all_scheduled_itinerary_events( cur )


def clear_all_guest_scheduled_item_schedules( conn: Connection ) -> None:
   cur = conn.cursor()

   try:
      _clear_guest_scheduled_item_schedules( cur )
      conn.commit()

   finally:
      cur.close()


def clear_all_itinerary_schedules( conn: Connection ) -> None:
   cur = conn.cursor()

   try:
      _clear_guest_scheduled_item_schedules( cur )
      ItineraryWalkRouteProvider.clear_itinerary_walk_route( cur )
      conn.commit()

   finally:
      cur.close()
