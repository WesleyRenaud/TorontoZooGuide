from __future__ import annotations

from .itinerary_animal_record import ItineraryAnimalRecord
from ...transportation.data_access.transportation_animal_record import TransportationAnimalRecord
from ...types import Types


class ItineraryTransportationAnimalProvider():
   @classmethod
   def insert_added_by_transportation(
         cls,
         cur: Types.Cursor,
         link: TransportationAnimalRecord,
         *,
         new_likelihood: int ) -> None:
      cur.execute(
         """   INSERT OR IGNORE INTO ItineraryAnimal (
                     SPECIES,
                     EXHIBIT,
                     ENCLOSURE_NAME,
                     OLD_LIKELIHOOD,
                     NEW_LIKELIHOOD,
                     IS_ADDED,
                     COVERED_BY_TALK,
                     ADDED_BY_TRANSPORTATION,
                     START_TIME,
                     END_TIME
                  )
                  VALUES ( ?, ?, ?, NULL, ?, 0, 0, 1, NULL, NULL );
         """,
         ( link.species, link.exhibit, link.enclosure_name, new_likelihood ),
      )


   @classmethod
   def update_added_by_transportation_likelihood(
         cls,
         cur: Types.Cursor,
         link: TransportationAnimalRecord,
         *,
         new_likelihood: int ) -> None:
      cur.execute(
         """   UPDATE ItineraryAnimal
               SET OLD_LIKELIHOOD = NEW_LIKELIHOOD,
                   NEW_LIKELIHOOD = ?
               WHERE ADDED_BY_TRANSPORTATION = 1
                 AND SPECIES = ?
                 AND EXHIBIT = ?
                 AND ENCLOSURE_NAME IS ?;
         """,
         ( new_likelihood, link.species, link.exhibit, link.enclosure_name ),
      )


   @classmethod
   def delete_added_by_transportation(
         cls,
         cur: Types.Cursor,
         animal: ItineraryAnimalRecord ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryAnimal
               WHERE ADDED_BY_TRANSPORTATION = 1
                 AND SPECIES = ?
                 AND EXHIBIT = ?
                 AND ENCLOSURE_NAME IS ?;
         """,
         ( animal.species, animal.exhibit, animal.enclosure_name ),
      )
