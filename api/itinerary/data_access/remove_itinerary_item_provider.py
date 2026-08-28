from __future__ import annotations

from .itinerary_transportation_provider import ItineraryTransportationProvider
from ...shared.enums import ItineraryEventType
from ...types import Types


class RemoveItineraryItemProvider():
   @classmethod
   def delete_itinerary_animal(
         cls,
         cur: Types.Cursor,
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


   @classmethod
   def delete_itinerary_attraction(
         cls,
         cur: Types.Cursor,
         *,
         name: str ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryAttraction
               WHERE ATTRACTION = ?;
            """,
         ( name, ),
      )


   @classmethod
   def delete_itinerary_transportation(
         cls,
         cur: Types.Cursor,
         name: str,
         added_as_attraction: bool ) -> None:
      ItineraryTransportationProvider.delete_itinerary_transportation(
         cur,
         transportation=name,
         added_as_attraction=added_as_attraction )


   @classmethod
   def delete_itinerary_guardians_talk(
         cls,
         cur: Types.Cursor,
         *,
         talk_name: str ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryGuardiansTalk
               WHERE TALK_NAME = ?;
            """,
         ( talk_name, ),
      )


   @classmethod
   def delete_itinerary_wild_encounter(
         cls,
         cur: Types.Cursor,
         *,
         wild_encounter: str ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryWildEncounter
               WHERE WILD_ENCOUNTER = ?;
            """,
         ( wild_encounter, ),
      )


   @classmethod
   def delete_itinerary_event(
         cls,
         cur: Types.Cursor,
         *,
         event_type: ItineraryEventType ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryEvent
               WHERE EVENT_TYPE = ?;
            """,
         ( event_type.value, ),
      )
