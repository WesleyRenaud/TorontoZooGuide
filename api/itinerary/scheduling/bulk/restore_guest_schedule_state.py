from __future__ import annotations

from ...data_access.fetch_itinerary_walk_route import fetch_itinerary_walk_route
from ...data_access.itinerary_time import set_itinerary_arrival_time
from ...data_access.itinerary_time import set_itinerary_departure_time
from ...data_access.save_itinerary_walk_route import save_itinerary_walk_route
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.schedule_itinerary_item import insert_itinerary_event_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_animal_cover_and_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_attraction_schedule
from ....models import ItineraryEvent
from ...routing.itinerary_walk_route import ItineraryWalkRoute
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ....types import ScheduleTimeKey
from ..unscheduling.clear_all_itinerary_schedules import clear_all_itinerary_schedules


def _has_schedule_times(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   return bool(
      DateValues.normalize_schedule_time_key( start_time )
      and DateValues.normalize_schedule_time_key( end_time ) )


def snapshot_guest_schedule_state(
      conn: Connection,
      saved_itinerary: SavedItinerary ) -> tuple[
         SavedItinerary,
         ItineraryWalkRoute,
      ]:
   return ( saved_itinerary, fetch_itinerary_walk_route( conn ) )


def restore_guest_schedule_state(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      walk_route: ItineraryWalkRoute ) -> None:
   clear_all_itinerary_schedules( conn )

   cur = conn.cursor()

   try:
      for animal_row in saved_itinerary.animal_rows:
         if not _has_schedule_times(
               animal_row.start_time,
               animal_row.end_time ):
            continue

         if animal_row.covered_by_talk:
            update_itinerary_animal_cover_and_schedule(
               cur,
               species=animal_row.species,
               exhibit=animal_row.exhibit,
               enclosure_name=animal_row.enclosure_name,
               covered_by_talk=True,
               start_time=animal_row.start_time,
               end_time=animal_row.end_time )
         else:
            update_itinerary_animal_schedule(
               cur,
               species=animal_row.species,
               exhibit=animal_row.exhibit,
               enclosure_name=animal_row.enclosure_name,
               start_time=animal_row.start_time,
               end_time=animal_row.end_time )

      for attraction_row in saved_itinerary.attraction_rows:
         if not _has_schedule_times(
               attraction_row.start_time,
               attraction_row.end_time ):
            continue

         update_itinerary_attraction_schedule(
            cur,
            name=attraction_row.attraction,
            start_time=attraction_row.start_time,
            end_time=attraction_row.end_time )

      for event_row in saved_itinerary.event_rows:
         insert_itinerary_event_schedule(
            cur,
            ItineraryEvent(
               event_type=event_row.event_type,
               start_time=event_row.start_time,
               end_time=event_row.end_time ) )

      conn.commit()

   finally:
      cur.close()

   set_itinerary_arrival_time( conn, saved_itinerary.arrival_time )
   set_itinerary_departure_time( conn, saved_itinerary.departure_time )
   save_itinerary_walk_route( conn, walk_route )
