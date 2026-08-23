from __future__ import annotations

from .itinerary_transportation import delete_itinerary_transportation as delete_itinerary_transportation_row
from ...shared.enums import ItineraryEventType
from ...types import Cursor


def delete_itinerary_animal(
      cur: Cursor,
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?
              AND ENCLOSURE_NAME IS ?;
         """,
      ( species, exhibit, enclosure_name ),
   )


def delete_itinerary_attraction(
      cur: Cursor,
      *,
      name: str ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
         """,
      ( name, ),
   )


def delete_itinerary_transportation(
      cur: Cursor,
      name: str,
      added_as_attraction: bool ) -> None:
   delete_itinerary_transportation_row(
      cur,
      transportation=name,
      added_as_attraction=added_as_attraction )


def delete_itinerary_guardians_talk(
      cur: Cursor,
      *,
      talk_name: str ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryGuardiansTalk
            WHERE TALK_NAME = ?;
         """,
      ( talk_name, ),
   )


def delete_itinerary_wild_encounter(
      cur: Cursor,
      *,
      wild_encounter: str ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = ?;
         """,
      ( wild_encounter, ),
   )


def delete_itinerary_event(
      cur: Cursor,
      *,
      event_type: ItineraryEventType ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryEvent
            WHERE EVENT_TYPE = ?;
         """,
      ( event_type.value, ),
   )
