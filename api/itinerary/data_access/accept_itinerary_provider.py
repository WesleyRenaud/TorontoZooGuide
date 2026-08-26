from __future__ import annotations

from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_transportation_provider import ItineraryTransportationProvider
from ...shared.constants import ITINERARY_ANIMAL_MIN_LIKELIHOOD
from ...types import Connection, Cursor


class AcceptItineraryProvider():
   @classmethod
   def build_excluded_animal_where_clause(
         cls,
         animals_to_keep: list[ ItineraryAnimalInput ] ) -> tuple[ str, list[ str ] ]:
      if not animals_to_keep:
         return '', []

      clauses: list[ str ] = []
      params: list[ str ] = []

      for animal in animals_to_keep:
         clauses.append(
            '( SPECIES = ? AND EXHIBIT = ? AND ENCLOSURE_NAME IS ? )' )
         params.extend( [
            animal.species,
            animal.exhibit,
            animal.enclosure_name,
         ] )

      return f" AND NOT ( { ' OR '.join( clauses ) } )", params


   @classmethod
   def remove_declined_itinerary_animals(
         cls,
         cur: Cursor,
         animals_to_keep: list[ ItineraryAnimalInput ] ) -> None:
      exclusion_clause, exclusion_params = cls.build_excluded_animal_where_clause( animals_to_keep )
      cur.execute(
         f"""   DELETE FROM ItineraryAnimal
                WHERE OLD_LIKELIHOOD IS NOT NULL
                   AND NEW_LIKELIHOOD IS NOT NULL
                   AND NEW_LIKELIHOOD < ?
                   { exclusion_clause };
         """,
         ( ITINERARY_ANIMAL_MIN_LIKELIHOOD, *exclusion_params ) )


   @classmethod
   def clear_added_itinerary_animals( cls, cur: Cursor ) -> None:
      cur.execute(
         """   UPDATE ItineraryAnimal
               SET IS_ADDED = 0
               WHERE IS_ADDED = 1;
         """ )


   @classmethod
   def clear_itinerary_animal_old_likelihoods( cls, cur: Cursor ) -> None:
      cur.execute(
         """   UPDATE ItineraryAnimal
               SET OLD_LIKELIHOOD = NULL
               WHERE OLD_LIKELIHOOD IS NOT NULL;
         """ )


   @classmethod
   def build_excluded_name_where_clause(
         cls,
         column: str,
         names_to_keep: list[ str ] ) -> tuple[ str, list[ str ] ]:
      if not names_to_keep:
         return '', []

      clauses = [ f'{ column } = ?' for _ in names_to_keep ]

      return f" AND NOT ( { ' OR '.join( clauses ) } )", names_to_keep


   @classmethod
   def remove_declined_itinerary_attractions(
         cls,
         cur: Cursor,
         attractions_to_keep: list[ str ] ) -> None:
      exclusion_clause, exclusion_params = cls.build_excluded_name_where_clause(
         'ATTRACTION',
         attractions_to_keep )
      cur.execute(
         f"""   DELETE FROM ItineraryAttraction
               WHERE OLD_LIKELIHOOD IS NOT NULL
                  AND NEW_LIKELIHOOD IS NOT NULL
                  AND NEW_LIKELIHOOD = 0
                  { exclusion_clause };
         """,
         exclusion_params )


   @classmethod
   def remove_declined_itinerary_transportations(
         cls,
         cur: Cursor,
         transportations_to_keep: list[ str ] ) -> None:
      exclusion_clause, exclusion_params = cls.build_excluded_name_where_clause(
         'TRANSPORTATION',
         transportations_to_keep )
      declined_rows = cur.execute(
         f"""   SELECT TRANSPORTATION, ADDED_AS_ATTRACTION
               FROM ItineraryTransportation
               WHERE OLD_LIKELIHOOD IS NOT NULL
                 AND NEW_LIKELIHOOD IS NOT NULL
                 AND NEW_LIKELIHOOD = 0
                 { exclusion_clause };
         """,
         exclusion_params ).fetchall()

      for row in declined_rows:
         ItineraryTransportationProvider.delete_itinerary_transportation(
            cur,
            transportation=row[ 'TRANSPORTATION' ],
            added_as_attraction=bool( row[ 'ADDED_AS_ATTRACTION' ] ) )


   @classmethod
   def clear_itinerary_attraction_old_likelihoods( cls, cur: Cursor ) -> None:
      cur.execute(
         """   UPDATE ItineraryAttraction
               SET OLD_LIKELIHOOD = NULL
               WHERE OLD_LIKELIHOOD IS NOT NULL;
         """ )


   @classmethod
   def clear_itinerary_transportation_old_likelihoods( cls, cur: Cursor ) -> None:
      cur.execute(
         """   UPDATE ItineraryTransportation
               SET OLD_LIKELIHOOD = NULL
               WHERE OLD_LIKELIHOOD IS NOT NULL;
         """ )


   @classmethod
   def remove_deleted_itinerary_guardians_talks( cls, cur: Cursor ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryGuardiansTalk
               WHERE IS_DELETED = 1;
         """ )


   @classmethod
   def remove_deleted_itinerary_wild_encounters( cls, cur: Cursor ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryWildEncounter
               WHERE IS_DELETED = 1;
         """ )


   @classmethod
   def accept_itinerary(
         cls,
         conn: Connection,
         animals_to_keep: list[ ItineraryAnimalInput ] | None = None,
         attractions_to_keep: list[ str ] | None = None ) -> bool:
      animals_to_keep = animals_to_keep or []
      attractions_to_keep = attractions_to_keep or []
      cur = conn.cursor()

      try:
         cls.remove_declined_itinerary_animals( cur, animals_to_keep=animals_to_keep )
         cls.remove_declined_itinerary_attractions(
            cur,
            attractions_to_keep=attractions_to_keep )
         cls.remove_declined_itinerary_transportations(
            cur,
            transportations_to_keep=attractions_to_keep )
         cls.clear_added_itinerary_animals( cur )
         cls.clear_itinerary_animal_old_likelihoods( cur )
         cls.clear_itinerary_attraction_old_likelihoods( cur )
         cls.clear_itinerary_transportation_old_likelihoods( cur )
         cls.remove_deleted_itinerary_guardians_talks( cur )
         cls.remove_deleted_itinerary_wild_encounters( cur )

         conn.commit()

      finally:
         cur.close()

      return True
