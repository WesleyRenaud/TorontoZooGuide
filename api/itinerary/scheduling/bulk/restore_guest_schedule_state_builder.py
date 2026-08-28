from __future__ import annotations

from ...data_access.itinerary_time_provider import ItineraryTimeProvider
from ...data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from ....models import ItineraryEvent
from ...routing.itinerary_walk_route import ItineraryWalkRoute
from ....shared.calendar_dates import DateValues
from ....types import Types
from ..unscheduling.itinerary_schedule_clearer import ItineraryScheduleClearer


class RestoreGuestScheduleStateBuilder():
   @classmethod
   def snapshot(
         cls,
         conn: Types.Connection,
         saved_itinerary: SavedItinerary ) -> tuple[
            SavedItinerary,
            ItineraryWalkRoute,
         ]:
      return (
         saved_itinerary,
         ItineraryWalkRouteProvider.fetch_itinerary_walk_route( conn ) )


   @classmethod
   def restore(
         cls,
         conn: Types.Connection,
         saved_itinerary: SavedItinerary,
         walk_route: ItineraryWalkRoute ) -> None:
      ItineraryScheduleClearer.clear_all( conn )

      cur = conn.cursor()

      try:
         for animal_row in saved_itinerary.animal_rows:
            if not cls._has_schedule_times(
                  animal_row.start_time,
                  animal_row.end_time ):
               continue

            if animal_row.covered_by_talk:
               ScheduleItineraryItemProvider.update_itinerary_animal_cover_and_schedule(
                  cur,
                  species=animal_row.species,
                  exhibit=animal_row.exhibit,
                  enclosure_name=animal_row.enclosure_name,
                  covered_by_talk=True,
                  start_time=animal_row.start_time,
                  end_time=animal_row.end_time )
            else:
               ScheduleItineraryItemProvider.update_itinerary_animal_schedule(
                  cur,
                  species=animal_row.species,
                  exhibit=animal_row.exhibit,
                  enclosure_name=animal_row.enclosure_name,
                  start_time=animal_row.start_time,
                  end_time=animal_row.end_time )

         for attraction_row in saved_itinerary.attraction_rows:
            if not cls._has_schedule_times(
                  attraction_row.start_time,
                  attraction_row.end_time ):
               continue

            ScheduleItineraryItemProvider.update_itinerary_attraction_schedule(
               cur,
               name=attraction_row.attraction,
               start_time=attraction_row.start_time,
               end_time=attraction_row.end_time )

         for event_row in saved_itinerary.event_rows:
            ScheduleItineraryItemProvider.insert_itinerary_event_schedule(
               cur,
               ItineraryEvent(
                  event_type=event_row.event_type,
                  start_time=event_row.start_time,
                  end_time=event_row.end_time ) )

         conn.commit()

      finally:
         cur.close()

      ItineraryTimeProvider.set_itinerary_arrival_time(
         conn,
         saved_itinerary.arrival_time )
      ItineraryTimeProvider.set_itinerary_departure_time(
         conn,
         saved_itinerary.departure_time )
      ItineraryWalkRouteProvider.save_itinerary_walk_route( conn, walk_route )


   @classmethod
   def _has_schedule_times(
         cls,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> bool:
      return bool(
         DateValues.normalize_schedule_time_key( start_time )
         and DateValues.normalize_schedule_time_key( end_time ) )
