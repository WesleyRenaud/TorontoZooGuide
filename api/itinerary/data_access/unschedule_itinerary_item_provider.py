from __future__ import annotations

from .itinerary_transportation_provider import ItineraryTransportationProvider
from .itinerary_transportation_route_marker_provider import ItineraryTransportationRouteMarkerProvider
from ...shared.enums import ItineraryEventType
from ...types import Cursor


class UnscheduleItineraryItemProvider():
   @classmethod
   def clear_all_itinerary_animal_schedules( cls, cur: Cursor ) -> None:
      cur.execute(
         """   UPDATE ItineraryAnimal
               SET START_TIME = NULL,
                   END_TIME = NULL,
                   COVERED_BY_TALK = 0;
            """ )


   @classmethod
   def clear_all_itinerary_attraction_schedules( cls, cur: Cursor ) -> None:
      cur.execute(
         """   UPDATE ItineraryAttraction
               SET START_TIME = NULL,
                   END_TIME = NULL;
            """ )


   @classmethod
   def clear_all_itinerary_transportation_schedules( cls, cur: Cursor ) -> None:
      ItineraryTransportationRouteMarkerProvider.clear_itinerary_transportation_route_markers( cur )
      ItineraryTransportationProvider.clear_itinerary_transportation_legs( cur )
      ItineraryTransportationProvider.clear_all_itinerary_transportation_schedule_times( cur )


   @classmethod
   def clear_all_scheduled_itinerary_events( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryEvent;' )


   @classmethod
   def clear_itinerary_animal_schedule(
         cls,
         cur: Cursor,
         *,
         species: str,
         exhibit: str,
         enclosure_name: str | None = None ) -> None:
      cur.execute(
         """   UPDATE ItineraryAnimal
               SET START_TIME = NULL,
                   END_TIME = NULL,
                   COVERED_BY_TALK = 0
               WHERE SPECIES = ?
                 AND EXHIBIT = ?
                 AND ENCLOSURE_NAME IS ?;
            """,
         ( species, exhibit, enclosure_name ),
      )


   @classmethod
   def clear_itinerary_attraction_schedule(
         cls,
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


   @classmethod
   def clear_itinerary_transportation_schedule(
         cls,
         cur: Cursor,
         name: str,
         added_as_attraction: bool ) -> None:
      ItineraryTransportationRouteMarkerProvider.delete_itinerary_transportation_route_markers(
         cur,
         transportation=name,
         added_as_attraction=added_as_attraction )
      ItineraryTransportationProvider.delete_itinerary_transportation_legs(
         cur,
         transportation=name,
         added_as_attraction=added_as_attraction )
      ItineraryTransportationProvider.clear_itinerary_transportation_schedule_times(
         cur,
         transportation=name,
         added_as_attraction=added_as_attraction )


   @classmethod
   def clear_itinerary_guardians_talk_schedule(
         cls,
         cur: Cursor,
         *,
         talk_name: str ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryGuardiansTalk
               WHERE TALK_NAME = ?;
            """,
         ( talk_name, ),
      )


   @classmethod
   def clear_itinerary_wild_encounter_schedule(
         cls,
         cur: Cursor,
         *,
         wild_encounter: str ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryWildEncounter
               WHERE WILD_ENCOUNTER = ?;
            """,
         ( wild_encounter, ),
      )


   @classmethod
   def delete_itinerary_event_schedule(
         cls,
         cur: Cursor,
         *,
         event_type: ItineraryEventType ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryEvent
               WHERE EVENT_TYPE = ?;
            """,
         ( event_type.value, ),
      )
