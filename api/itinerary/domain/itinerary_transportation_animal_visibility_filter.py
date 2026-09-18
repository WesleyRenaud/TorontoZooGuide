from __future__ import annotations

from ...animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from ...models import Animal
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...request_connection_provider import RequestConnectionProvider
from ...transportation.data_access.transportation_animal_provider import TransportationAnimalProvider
from ...transportation.data_access.transportation_animal_record import TransportationAnimalRecord


class ItineraryTransportationAnimalVisibilityFilter():
   @classmethod
   def apply(
         cls,
         animals: list[ Animal ],
         *,
         itinerary_legs: list[ ItineraryTransportationLeg ] ) -> list[ Animal ]:
      if not any( animal.added_by_transportation for animal in animals ):
         return animals

      present_leg_keys = {
         ( leg.transportation, leg.from_station, leg.to_station )
         for leg in itinerary_legs
      }
      catalog_by_spot = {
         link.viewing_spot_key(): link
         for link in TransportationAnimalProvider.fetch_all(
            RequestConnectionProvider.get() )
      }

      return [
         animal
         for animal in animals
         if cls._is_visible(
            animal,
            catalog_by_spot,
            present_leg_keys )
      ]


   @classmethod
   def _is_visible(
         cls,
         animal: Animal,
         catalog_by_spot: dict[ tuple[ str, str, str | None ], TransportationAnimalRecord ],
         present_leg_keys: set[ tuple[ str, str, str ] ] ) -> bool:
      if not animal.added_by_transportation:
         return True

      link = catalog_by_spot.get( ViewingSpotKeyBuilder.from_animal( animal ) )

      if link is None:
         return False

      return link.leg_key() in present_leg_keys
