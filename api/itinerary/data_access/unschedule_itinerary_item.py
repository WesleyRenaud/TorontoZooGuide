from __future__ import annotations

from ...shared.enums import ItineraryEventType
from ...types import Cursor


def clear_all_itinerary_animal_schedules( cur: Cursor ) -> None:
   cur.execute(
      """   UPDATE ItineraryAnimal
            SET START_TIME = NULL,
                END_TIME = NULL;
         """ )


def clear_all_itinerary_attraction_schedules( cur: Cursor ) -> None:
   cur.execute(
      """   UPDATE ItineraryAttraction
            SET START_TIME = NULL,
                END_TIME = NULL;
         """ )


def clear_itinerary_animal_schedule(
      cur: Cursor,
      *,
      species: str,
      exhibit: str ) -> None:
   cur.execute(
      """   UPDATE ItineraryAnimal
            SET START_TIME = NULL,
                END_TIME = NULL
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
         """,
      ( species, exhibit ),
   )


def clear_itinerary_attraction_schedule(
      cur: Cursor,
      *,
      name: str ) -> None:
   cur.execute(
      """   UPDATE ItineraryAttraction
            SET START_TIME = NULL,
                END_TIME = NULL
            WHERE ATTRACTION = ?;
         """,
      ( name, ),
   )


def clear_itinerary_guardians_talk_schedule(
      cur: Cursor,
      *,
      talk_name: str ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryGuardiansTalk
            WHERE TALK_NAME = ?;
         """,
      ( talk_name, ),
   )


def clear_itinerary_wild_encounter_schedule(
      cur: Cursor,
      *,
      wild_encounter: str ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = ?;
         """,
      ( wild_encounter, ),
   )


def delete_itinerary_event_schedule(
      cur: Cursor,
      *,
      event_type: ItineraryEventType ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
         """,
      ( event_type.value, ),
   )
