from __future__ import annotations

from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryEventType
from ...types import Connection, ScheduleTimeKey


def schedule_time_occurs_outside_visit_window(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> bool:
   if start_time is None or end_time is None:
      return False

   return (
      DateValues.time_value_is_before( start_time, arrival_time )
      or DateValues.time_value_is_after( end_time, departure_time )
   )


def cleared_schedule_times_for_visit_window(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ]:
   if schedule_time_occurs_outside_visit_window(
         start_time,
         end_time,
         arrival_time=arrival_time,
         departure_time=departure_time ):
      return ( None, None )

   return ( start_time, end_time )


def clear_schedules_outside_visit_window(
      conn: Connection,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> bool:
   cur = conn.cursor()
   did_clear_schedule = False

   try:
      for animal in ItineraryProvider.fetch_itinerary_animal_rows( conn ):
         if not schedule_time_occurs_outside_visit_window(
               animal.start_time,
               animal.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            continue

         UnscheduleItineraryItemProvider.clear_itinerary_animal_schedule(
            cur,
            species=animal.species,
            exhibit=animal.exhibit )
         did_clear_schedule = True

      for attraction in ItineraryProvider.fetch_itinerary_attraction_rows( conn ):
         if not schedule_time_occurs_outside_visit_window(
               attraction.start_time,
               attraction.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            continue

         UnscheduleItineraryItemProvider.clear_itinerary_attraction_schedule(
            cur,
            name=attraction.attraction )
         did_clear_schedule = True

      for transportation in ItineraryProvider.fetch_itinerary_transportation_rows( conn ):
         if not schedule_time_occurs_outside_visit_window(
               transportation.start_time,
               transportation.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            continue

         UnscheduleItineraryItemProvider.clear_itinerary_transportation_schedule(
            cur,
            name=transportation.transportation,
            added_as_attraction=transportation.added_as_attraction )
         did_clear_schedule = True

      for event in ItineraryProvider.fetch_itinerary_event_rows( conn ):
         if event.event_type in (
               ItineraryEventType.ARRIVAL,
               ItineraryEventType.DEPARTURE ):
            continue

         if not schedule_time_occurs_outside_visit_window(
               event.start_time,
               event.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            continue

         UnscheduleItineraryItemProvider.delete_itinerary_event_schedule(
            cur,
            event_type=event.event_type )
         did_clear_schedule = True

      if did_clear_schedule:
         conn.commit()

   finally:
      cur.close()

   return did_clear_schedule
