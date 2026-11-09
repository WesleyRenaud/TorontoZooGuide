from __future__ import annotations

from ...animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from ...models.animal import Animal
from ...transportation.data_access.transportation_animal_record import TransportationAnimalRecord
from ...walk_graph.domain.viewing_spot_name_key import ViewingSpotNameKey


class ItineraryTransportationAnimalLikelihoodLookup:
   _likelihood_by_spot: dict[ ViewingSpotNameKey, int ]


   def __init__( self, animals: list[ Animal ] ) -> None:
      spots: dict[ ViewingSpotNameKey, int ] = {}

      for animal in animals:
         species, exhibit, enclosure_name = ViewingSpotKeyBuilder.from_animal( animal )
         spots[ ViewingSpotNameKey( species, exhibit, enclosure_name ) ] = animal.likelihood or 0

      self._likelihood_by_spot = spots


   def for_link( self, link: TransportationAnimalRecord ) -> int:
      return self._likelihood_by_spot.get( link.viewing_spot_key(), 0 )
