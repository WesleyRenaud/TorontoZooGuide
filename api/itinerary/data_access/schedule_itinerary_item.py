from __future__ import annotations

from ...models.itinerary_event import ItineraryEvent
from ...shared.date_values import DateValues
from ...types import Cursor, ScheduleTimeKey


def update_itinerary_animal_schedule(
      cur: Cursor,
      *,
      species: str,
      exhibit: str,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   cur.execute(
      """   UPDATE ItineraryAnimal
            SET START_TIME = ?,
                END_TIME = ?
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
         """,
         (
            DateValues.normalize_itinerary_schedule_time( start_time ),
            DateValues.normalize_itinerary_schedule_time( end_time ),
            species,
            exhibit,
         ),
   )

   return cur.rowcount > 0


def update_itinerary_attraction_schedule(
      cur: Cursor,
      *,
      name: str,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   cur.execute(
      """   UPDATE ItineraryAttraction
            SET START_TIME = ?,
                END_TIME = ?
            WHERE ATTRACTION = ?;
         """,
         (
            DateValues.normalize_itinerary_schedule_time( start_time ),
            DateValues.normalize_itinerary_schedule_time( end_time ),
            name,
         ),
   )

   return cur.rowcount > 0


def insert_itinerary_event_schedule(
      cur: Cursor,
      event: ItineraryEvent ) -> None:
   cur.execute(
      """   INSERT OR IGNORE INTO ItineraryEvent (
                  EVENT_TYPE,
                  START_TIME,
                  END_TIME
               )
               VALUES ( ?, ?, ? );
         """,
         (
            event.event_type.value,
            DateValues.normalize_itinerary_schedule_time( event.start_time ),
            DateValues.normalize_itinerary_schedule_time( event.end_time ),
         ),
   )
