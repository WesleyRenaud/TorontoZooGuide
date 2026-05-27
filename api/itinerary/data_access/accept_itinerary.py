from __future__ import annotations

from ...types import Connection, Cursor


def remove_declined_itinerary_animals( cur: Cursor ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryAnimal
            WHERE OLD_LIKELIHOOD IS NOT NULL
               AND NEW_LIKELIHOOD IS NOT NULL
               AND NEW_LIKELIHOOD = 0;
      """ )


def clear_added_itinerary_animals( cur: Cursor ) -> None:
   cur.execute(
      """   UPDATE ItineraryAnimal
            SET IS_ADDED = 0
            WHERE IS_ADDED = 1;
      """ )

def clear_itinerary_animal_old_likelihoods( cur: Cursor ) -> None:
   cur.execute(
      """   UPDATE ItineraryAnimal
            SET OLD_LIKELIHOOD = NULL
            WHERE OLD_LIKELIHOOD IS NOT NULL;
      """ )


def remove_declined_itinerary_attractions( cur: Cursor ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryAttraction
            WHERE OLD_LIKELIHOOD IS NOT NULL
               AND NEW_LIKELIHOOD IS NOT NULL
               AND NEW_LIKELIHOOD < OLD_LIKELIHOOD;
      """ )

def clear_itinerary_attraction_old_likelihoods( cur: Cursor ) -> None:
   cur.execute(
      """   UPDATE ItineraryAttraction
            SET OLD_LIKELIHOOD = NULL
            WHERE OLD_LIKELIHOOD IS NOT NULL;
      """ )


def remove_deleted_itinerary_guardians_talks( cur: Cursor ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryGuardiansTalk
            WHERE IS_DELETED = 1;
      """ )


def remove_deleted_itinerary_wild_encounters( cur: Cursor ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryWildEncounter
            WHERE IS_DELETED = 1;
      """ )


def accept_itinerary( conn: Connection ) -> bool:
   cur = conn.cursor()

   try:
      # TO-DO: Evatually we will support overriding behaviour here for animals and attractions
      remove_declined_itinerary_animals( cur )
      remove_declined_itinerary_attractions( cur )
      clear_added_itinerary_animals( cur )
      clear_itinerary_animal_old_likelihoods( cur )
      clear_itinerary_attraction_old_likelihoods( cur )
      remove_deleted_itinerary_guardians_talks( cur )
      remove_deleted_itinerary_wild_encounters( cur )

      conn.commit()

   finally:
      cur.close()

   return True
