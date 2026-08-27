from __future__ import annotations

from ..core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from ...data_access.saved_itinerary import SavedItinerary


class GuestScheduledItineraryItemChecker():
   @classmethod
   def has_items(
         cls,
         saved_itinerary: SavedItinerary ) -> bool:
      for animal_row in saved_itinerary.animal_rows:
         if GuestItemScheduleStatusChecker.has_schedule_times(
               animal_row.start_time,
               animal_row.end_time ):
            return True

      for attraction_row in saved_itinerary.attraction_rows:
         if GuestItemScheduleStatusChecker.has_schedule_times(
               attraction_row.start_time,
               attraction_row.end_time ):
            return True

      for transportation_row in saved_itinerary.transportation_rows:
         if GuestItemScheduleStatusChecker.has_schedule_times(
               transportation_row.start_time,
               transportation_row.end_time ):
            return True

      if saved_itinerary.event_rows:
         return True

      return False
