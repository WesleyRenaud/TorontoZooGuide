from __future__ import annotations

from ...types import Connection, Cursor


def clear_itinerary_date( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryDate;' )


def clear_itinerary_animals( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryAnimal;' )


def clear_itinerary_attractions( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryAttraction;' )


def clear_itinerary_guardians_talks( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryGuardiansTalk;' )


def clear_itinerary_wild_encounters( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryWildEncounter;' )


def clear_itinerary( conn: Connection ) -> bool:
   cur = conn.cursor()

   try:
      clear_itinerary_date( cur )
      clear_itinerary_animals( cur )
      clear_itinerary_attractions( cur )
      clear_itinerary_guardians_talks( cur )
      clear_itinerary_wild_encounters( cur )

      conn.commit()

   finally:
      cur.close()

   return True
