from __future__ import annotations

from api.itinerary.domain.itinerary_transportation_animal_likelihood_lookup import ItineraryTransportationAnimalLikelihoodLookup
from api.models.animal import Animal
from api.transportation.data_access.transportation_animal_record import TransportationAnimalRecord


GIRAFFE_LINK = TransportationAnimalRecord(
   transportation='Zoomobile',
   from_station='Canadian Domain Zoomobile Station',
   to_station='Africa Zoomobile Station',
   species='Masai Giraffe',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)


def Test_ForLink_TestMatchingAnimal_ExpectLikelihood() -> None:
   likelihood = 80
   animal = Animal(
      species=GIRAFFE_LINK.species,
      exhibit=GIRAFFE_LINK.exhibit,
      enclosure_name=GIRAFFE_LINK.enclosure_name,
      likelihood=likelihood )
   lookup = ItineraryTransportationAnimalLikelihoodLookup( [ animal ] )

   resolved = lookup.for_link( GIRAFFE_LINK )

   assert resolved == animal.likelihood


def Test_ForLink_TestMissingSpot_ExpectZero() -> None:
   lookup = ItineraryTransportationAnimalLikelihoodLookup( [] )

   resolved = lookup.for_link( GIRAFFE_LINK )

   assert resolved == 0
