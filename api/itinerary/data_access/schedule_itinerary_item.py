from __future__ import annotations

from ...models.itinerary_event import ItineraryEvent
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryEventType
from ...types import Cursor, ScheduleTimeKey


def insert_itinerary_animal_schedule(
      cur: Cursor,
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   cur.execute(
      """   INSERT OR IGNORE INTO ItineraryAnimal (
                  SPECIES,
                  EXHIBIT,
                  ENCLOSURE_NAME,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD,
                  IS_ADDED,
                  START_TIME,
                  END_TIME
               )
               VALUES ( ?, ?, ?, ?, ?, ?, ?, ? );
         """,
         (
            species,
            exhibit,
            enclosure_name,
            None,
            None,
            False,
            DateValues.normalize_itinerary_schedule_time( start_time ),
            DateValues.normalize_itinerary_schedule_time( end_time ),
         ),
   )

   return cur.rowcount > 0


def insert_itinerary_attraction_schedule(
      cur: Cursor,
      *,
      name: str,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   cur.execute(
      """   INSERT OR IGNORE INTO ItineraryAttraction (
                  ATTRACTION,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD,
                  START_TIME,
                  END_TIME
               )
               VALUES ( ?, ?, ?, ?, ? );
         """,
         (
            name,
            None,
            None,
            DateValues.normalize_itinerary_schedule_time( start_time ),
            DateValues.normalize_itinerary_schedule_time( end_time ),
         ),
   )

   return cur.rowcount > 0


def update_itinerary_animal_schedule(
      cur: Cursor,
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   cur.execute(
      """   UPDATE ItineraryAnimal
            SET START_TIME = ?,
                END_TIME = ?
            WHERE SPECIES = ?
              AND EXHIBIT = ?
              AND ENCLOSURE_NAME IS ?;
         """,
         (
            DateValues.normalize_itinerary_schedule_time( start_time ),
            DateValues.normalize_itinerary_schedule_time( end_time ),
            species,
            exhibit,
            enclosure_name,
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


def update_itinerary_event_schedule(
      cur: Cursor,
      *,
      event_type: ItineraryEventType,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   cur.execute(
      """   UPDATE ItineraryEvent
            SET START_TIME = ?,
                END_TIME = ?
            WHERE EVENT_TYPE = ?;
         """,
         (
            DateValues.normalize_itinerary_schedule_time( start_time ),
            DateValues.normalize_itinerary_schedule_time( end_time ),
            event_type.value,
         ),
   )

   return cur.rowcount > 0


def insert_itinerary_guardians_talk(
      cur: Cursor,
      *,
      talk_name: str,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      is_deleted: bool = False ) -> bool:
   cur.execute(
      """   INSERT OR IGNORE INTO ItineraryGuardiansTalk (
                  TALK_NAME,
                  START_TIME,
                  END_TIME,
                  IS_DELETED
               )
               VALUES ( ?, ?, ?, ? );
         """,
         (
            talk_name,
            DateValues.normalize_itinerary_schedule_time( start_time ),
            DateValues.normalize_itinerary_schedule_time( end_time ),
            is_deleted,
         ),
   )

   return cur.rowcount > 0


def insert_itinerary_wild_encounter(
      cur: Cursor,
      *,
      wild_encounter_name: str,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      is_deleted: bool = False ) -> bool:
   cur.execute(
      """   INSERT OR IGNORE INTO ItineraryWildEncounter (
                  WILD_ENCOUNTER,
                  START_TIME,
                  END_TIME,
                  IS_DELETED
               )
               VALUES ( ?, ?, ?, ? );
         """,
         (
            wild_encounter_name,
            DateValues.normalize_schedule_time( start_time ),
            DateValues.normalize_schedule_time( end_time ),
            is_deleted,
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
