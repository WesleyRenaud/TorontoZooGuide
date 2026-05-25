from __future__ import annotations

from datetime import date

from ..data_access.validated_itinerary import ValidatedItinerary
from ...models.animal_diff import AnimalDiff
from ...models.attraction_diff import AttractionDiff
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ...types import Connection, Cursor


def save_itinerary_date( cur: Cursor, visit_date: date ) -> None:
   cur.execute(
      """   INSERT INTO ItineraryDate ( ITINERARY_DATE )
            VALUES ( ? );
      """,
      ( visit_date, ) )


def save_itinerary_animals( cur: Cursor, animals: list[ AnimalDiff ] ) -> None:
   if not animals:
      return

   for animal in animals:
      cur.execute(
         """   INSERT OR IGNORE INTO ItineraryAnimal (
                  SPECIES,
                  EXHIBIT,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD,
                  IS_ADDED
               )
               VALUES ( ?, ?, ?, ?, ? );
         """,
         (
            animal.species,
            animal.exhibit,
            animal.old_likelihood,
            animal.new_likelihood,
            animal.is_added,
         ) )


def save_itinerary_attractions( cur: Cursor, attractions: list[ AttractionDiff ] ) -> None:
   if not attractions:
      return

   for attraction in attractions:
      cur.execute(
         """   INSERT OR IGNORE INTO ItineraryAttraction (
                  ATTRACTION,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD
               )
               VALUES ( ?, ?, ? );
         """,
         (
            attraction.name,
            attraction.old_likelihood,
            attraction.new_likelihood,
         ) )


def save_itinerary_guardians_talks( cur: Cursor, guardians_talks: list[ GuardiansTalkDiff ] ) -> None:
   if not guardians_talks:
      return

   for talk in guardians_talks:
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
            talk.name,
            talk.start_time,
            talk.end_time,
            talk.is_deleted,
         ) )


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
            encounter.start_time,
            encounter.end_time,
            encounter.is_deleted,
         ) )


def save_validated_itinerary(
      conn: Connection,
      visit_date: date,
      validated_itinerary: ValidatedItinerary ) -> bool:
   cur = conn.cursor()

   try:
      save_itinerary_date( cur, visit_date )
      save_itinerary_animals( cur, validated_itinerary.animals )
      save_itinerary_attractions( cur, validated_itinerary.attractions )
      save_itinerary_guardians_talks( cur, validated_itinerary.guardians_talks )
      save_itinerary_wild_encounters( cur, validated_itinerary.wild_encounters )

      conn.commit()

   finally:
      cur.close()

   return True
