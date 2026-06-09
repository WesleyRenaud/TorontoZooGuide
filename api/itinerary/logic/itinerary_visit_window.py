from __future__ import annotations

from ..data_access.itinerary import fetch_itinerary_animal_rows
from ..data_access.itinerary import fetch_itinerary_attraction_rows
from ..data_access.itinerary import fetch_itinerary_event_rows
from ..data_access.itinerary import fetch_itinerary_guardians_talk_rows
from ..data_access.itinerary import fetch_itinerary_wild_encounter_rows
from ..data_access.unschedule_itinerary_item import clear_itinerary_animal_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_attraction_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_guardians_talk_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_wild_encounter_schedule
from ..data_access.unschedule_itinerary_item import delete_itinerary_event_schedule
from ...shared.date_values import DateValues
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
      for animal in fetch_itinerary_animal_rows( conn ):
         if not schedule_time_occurs_outside_visit_window(
               animal.start_time,
               animal.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            continue

         clear_itinerary_animal_schedule(
            cur,
            species=animal.species,
            exhibit=animal.exhibit )
         did_clear_schedule = True

      for attraction in fetch_itinerary_attraction_rows( conn ):
         if not schedule_time_occurs_outside_visit_window(
               attraction.start_time,
               attraction.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            continue

         clear_itinerary_attraction_schedule(
            cur,
            name=attraction.attraction )
         did_clear_schedule = True

      for talk in fetch_itinerary_guardians_talk_rows( conn ):
         if talk.is_deleted:
            continue

         if not schedule_time_occurs_outside_visit_window(
               talk.start_time,
               talk.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            continue

         clear_itinerary_guardians_talk_schedule(
            cur,
            talk_name=talk.talk_name )
         did_clear_schedule = True

      for encounter in fetch_itinerary_wild_encounter_rows( conn ):
         if encounter.is_deleted:
            continue

         if not schedule_time_occurs_outside_visit_window(
               encounter.start_time,
               encounter.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            continue

         clear_itinerary_wild_encounter_schedule(
            cur,
            wild_encounter=encounter.wild_encounter )
         did_clear_schedule = True

      for event in fetch_itinerary_event_rows( conn ):
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

         delete_itinerary_event_schedule(
            cur,
            event_type=event.event_type )
         did_clear_schedule = True

      if did_clear_schedule:
         conn.commit()

   finally:
      cur.close()

   return did_clear_schedule
