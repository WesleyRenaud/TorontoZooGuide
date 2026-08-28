from __future__ import annotations

from ...models.itinerary_event import ItineraryEvent
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryEventType
from ...types import Types


class ScheduleItineraryItemProvider():
   @classmethod
   def insert_itinerary_animal_schedule(
         cls,
         cur: Types.Cursor,
         *,
         species: str,
         exhibit: str,
         enclosure_name: str | None = None,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> bool:
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


   @classmethod
   def insert_itinerary_attraction_schedule(
         cls,
         cur: Types.Cursor,
         *,
         name: str,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> bool:
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


   @classmethod
   def update_itinerary_animal_schedule(
         cls,
         cur: Types.Cursor,
         *,
         species: str,
         exhibit: str,
         enclosure_name: str | None = None,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> bool:
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


   @classmethod
   def update_itinerary_animal_cover_and_schedule(
         cls,
         cur: Types.Cursor,
         *,
         species: str,
         exhibit: str,
         enclosure_name: str | None = None,
         covered_by_talk: bool,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> bool:
      cur.execute(
         """   UPDATE ItineraryAnimal
               SET START_TIME = ?,
                   END_TIME = ?,
                   COVERED_BY_TALK = ?
               WHERE SPECIES = ?
                 AND EXHIBIT = ?
                 AND ENCLOSURE_NAME IS ?;
            """,
            (
               DateValues.normalize_itinerary_schedule_time( start_time ),
               DateValues.normalize_itinerary_schedule_time( end_time ),
               covered_by_talk,
               species,
               exhibit,
               enclosure_name,
            ),
      )

      return cur.rowcount > 0


   @classmethod
   def update_itinerary_attraction_schedule(
         cls,
         cur: Types.Cursor,
         *,
         name: str,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> bool:
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


   @classmethod
   def update_itinerary_event_schedule(
         cls,
         cur: Types.Cursor,
         *,
         event_type: ItineraryEventType,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> bool:
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


   @classmethod
   def insert_itinerary_guardians_talk(
         cls,
         cur: Types.Cursor,
         *,
         talk_name: str,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey,
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


   @classmethod
   def insert_itinerary_wild_encounter(
         cls,
         cur: Types.Cursor,
         *,
         wild_encounter_name: str,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey,
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


   @classmethod
   def insert_itinerary_event_schedule(
         cls,
         cur: Types.Cursor,
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
