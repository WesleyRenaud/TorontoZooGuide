from __future__ import annotations

from .itinerary_animal_input import ItineraryAnimalInput
from ...types import Connection, Cursor


def build_excluded_animal_where_clause(
      animals_to_keep: list[ ItineraryAnimalInput ] ) -> tuple[ str, list[ str ] ]:
   if not animals_to_keep:
      return '', []

   clauses: list[ str ] = []
   params: list[ str ] = []

   for animal in animals_to_keep:
      clauses.append( '( SPECIES = ? AND EXHIBIT = ? )' )
      params.extend( [ animal.species, animal.exhibit ] )

   return f" AND NOT ( { ' OR '.join( clauses ) } )", params


def remove_declined_itinerary_animals(
      cur: Cursor,
      animals_to_keep: list[ ItineraryAnimalInput ] ) -> None:
   exclusion_clause, exclusion_params = build_excluded_animal_where_clause( animals_to_keep )
   cur.execute(
      f"""   DELETE FROM ItineraryAnimal
             WHERE OLD_LIKELIHOOD IS NOT NULL
                AND NEW_LIKELIHOOD IS NOT NULL
                AND NEW_LIKELIHOOD = 0
                { exclusion_clause };
      """,
      exclusion_params )


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


def build_excluded_attraction_where_clause(
      attractions_to_keep: list[ str ] ) -> tuple[ str, list[ str ] ]:
   if not attractions_to_keep:
      return '', []

   clauses: list[ str ] = []
   params: list[ str ] = []

   for attraction_name in attractions_to_keep:
      clauses.append( 'ATTRACTION = ?' )
      params.append( attraction_name )

   return f" AND NOT ( { ' OR '.join( clauses ) } )", params


def remove_declined_itinerary_attractions(
      cur: Cursor,
      attractions_to_keep: list[ str ] ) -> None:
   exclusion_clause, exclusion_params = build_excluded_attraction_where_clause(
      attractions_to_keep )
   cur.execute(
      f"""   DELETE FROM ItineraryAttraction
            WHERE OLD_LIKELIHOOD IS NOT NULL
               AND NEW_LIKELIHOOD IS NOT NULL
               AND NEW_LIKELIHOOD = 0
               { exclusion_clause };
      """,
      exclusion_params )

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


def accept_itinerary(
      conn: Connection,
      animals_to_keep: list[ ItineraryAnimalInput ] | None = None,
      attractions_to_keep: list[ str ] | None = None ) -> bool:
   animals_to_keep = animals_to_keep or []
   attractions_to_keep = attractions_to_keep or []
   cur = conn.cursor()

   try:
      remove_declined_itinerary_animals( cur, animals_to_keep=animals_to_keep )
      remove_declined_itinerary_attractions(
         cur,
         attractions_to_keep=attractions_to_keep )
      clear_added_itinerary_animals( cur )
      clear_itinerary_animal_old_likelihoods( cur )
      clear_itinerary_attraction_old_likelihoods( cur )
      remove_deleted_itinerary_guardians_talks( cur )
      remove_deleted_itinerary_wild_encounters( cur )

      conn.commit()

   finally:
      cur.close()

   return True
