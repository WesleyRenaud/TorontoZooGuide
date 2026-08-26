from __future__ import annotations

from .itinerary_transportation_provider import ItineraryTransportationProvider
from .itinerary_walk_route_provider import ItineraryWalkRouteProvider
from ...types import Connection, Cursor


class ClearItineraryProvider():
   @classmethod
   def clear_itinerary_date( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryDate;' )


   @classmethod
   def clear_itinerary_exhibits( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryExhibit;' )


   @classmethod
   def clear_itinerary_animals( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryAnimal;' )


   @classmethod
   def clear_itinerary_attractions( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryAttraction;' )


   @classmethod
   def clear_itinerary_guardians_talks( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryGuardiansTalk;' )


   @classmethod
   def clear_itinerary_wild_encounters( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryWildEncounter;' )


   @classmethod
   def clear_itinerary_events( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryEvent;' )


   @classmethod
   def clear_itinerary( cls, conn: Connection ) -> bool:
      cur = conn.cursor()

      try:
         cls.clear_itinerary_date( cur )
         cls.clear_itinerary_exhibits( cur )
         cls.clear_itinerary_animals( cur )
         cls.clear_itinerary_attractions( cur )
         ItineraryTransportationProvider.clear_itinerary_transportations( cur )
         cls.clear_itinerary_guardians_talks( cur )
         cls.clear_itinerary_wild_encounters( cur )
         cls.clear_itinerary_events( cur )
         ItineraryWalkRouteProvider.clear_itinerary_walk_route( cur )

         conn.commit()

      finally:
         cur.close()

      return True
