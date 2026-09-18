from __future__ import annotations

from ...animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from ...models.animal import Animal
from ...transportation.data_access.transportation_animal_record import TransportationAnimalRecord


class ItineraryTransportationAnimalLikelihoodLookup:
   def __init__( self, animals: list[ Animal ] ) -> None:
      self._likelihood_by_spot = {
         ViewingSpotKeyBuilder.from_animal( animal ): animal.likelihood
         for animal in animals
      }


   def for_link( self, link: TransportationAnimalRecord ) -> int:
      return self._likelihood_by_spot.get( link.viewing_spot_key(), 0 )
