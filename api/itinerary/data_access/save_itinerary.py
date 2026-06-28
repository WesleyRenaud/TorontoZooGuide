from __future__ import annotations

from datetime import date

from ...models.animal_diff import AnimalDiff
from ...models.attraction_diff import AttractionDiff
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.itinerary_event import ItineraryEvent
from ...models.wild_encounter_diff import WildEncounterDiff
from .schedule_itinerary_item import insert_itinerary_guardians_talk
from ...shared.calendar_dates import DateValues
from ...types import Connection, Cursor, ScheduleTimeKey
from .validated_itinerary import ValidatedItinerary


def save_itinerary_date(
      cur: Cursor,
      visit_date: date,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> None:
   cur.execute(
      """   INSERT INTO ItineraryDate (
               ITINERARY_DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      (
         visit_date,
         arrival_time,
         departure_time,
      ) )


def save_itinerary_animals( cur: Cursor, animals: list[ AnimalDiff ] ) -> None:
   if not animals:
      return

   for animal in animals:
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
            animal.species,
            animal.exhibit,
            animal.enclosure_name,
            animal.old_likelihood,
            animal.new_likelihood,
            animal.is_added,
            DateValues.normalize_itinerary_schedule_time( animal.start_time ),
            DateValues.normalize_itinerary_schedule_time( animal.end_time ),
         ) )


def save_itinerary_attractions( cur: Cursor, attractions: list[ AttractionDiff ] ) -> None:
   if not attractions:
      return

   for attraction in attractions:
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
            attraction.name,
            attraction.old_likelihood,
            attraction.new_likelihood,
            DateValues.normalize_itinerary_schedule_time( attraction.start_time ),
            DateValues.normalize_itinerary_schedule_time( attraction.end_time ),
         ) )


def save_itinerary_guardians_talks( cur: Cursor, guardians_talks: list[ GuardiansTalkDiff ] ) -> None:
   if not guardians_talks:
      return

   for talk in guardians_talks:
      insert_itinerary_guardians_talk(
         cur,
         talk_name=talk.name,
         start_time=talk.start_time,
         end_time=talk.end_time,
         is_deleted=talk.is_deleted,
      )


def save_itinerary_wild_encounters( cur: Cursor, wild_encounters: list[ WildEncounterDiff ] ) -> None:
   if not wild_encounters:
      return

   for encounter in wild_encounters:
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
            encounter.name,
            DateValues.normalize_schedule_time( encounter.start_time ),
            DateValues.normalize_schedule_time( encounter.end_time ),
            encounter.is_deleted,
         ) )


def save_itinerary_events( cur: Cursor, events: list[ ItineraryEvent ] ) -> None:
   if not events:
      return

   for event in events:
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
         ) )


def save_validated_itinerary(
      conn: Connection,
      visit_date: date,
      validated_itinerary: ValidatedItinerary ) -> bool:
   cur = conn.cursor()

   try:
      save_itinerary_date(
         cur,
         visit_date,
         validated_itinerary.arrival_time,
         validated_itinerary.departure_time )
      save_itinerary_animals( cur, validated_itinerary.animals )
      save_itinerary_attractions( cur, validated_itinerary.attractions )
      save_itinerary_guardians_talks( cur, validated_itinerary.guardians_talks )
      save_itinerary_wild_encounters( cur, validated_itinerary.wild_encounters )
      save_itinerary_events( cur, validated_itinerary.events )

      conn.commit()

   finally:
      cur.close()

   return True
