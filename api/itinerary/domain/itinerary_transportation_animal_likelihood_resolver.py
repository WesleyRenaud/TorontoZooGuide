from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_provider import ItineraryProvider
from .itinerary_transportation_animal_likelihood_lookup import ItineraryTransportationAnimalLikelihoodLookup
from ...request_connection_provider import RequestConnectionProvider
from ...shared.calendar_dates import DateValues
from ...transportation.data_access.transportation_animal_record import TransportationAnimalRecord
from ...types import Types


class ItineraryTransportationAnimalLikelihoodResolver():
   @classmethod
   def resolve(
         cls,
         conn: Types.Connection,
         links: list[ TransportationAnimalRecord ] ) -> ItineraryTransportationAnimalLikelihoodLookup:
      visit_date = DateValues.parse_date_value(
         ItineraryProvider.fetch_itinerary_date( conn ) )
      saved_animals = [
         ItineraryAnimalRecord(
            species=link.species,
            exhibit=link.exhibit,
            enclosure_name=link.enclosure_name,
            old_likelihood=None,
            new_likelihood=None )
         for link in links
      ]
      previous_connection = RequestConnectionProvider.get()

      try:
         RequestConnectionProvider.set( conn )
         animals = AnimalCoordinator.get_animals_for_saved_itinerary(
            day=visit_date.day,
            month=visit_date.month,
            year=visit_date.year,
            saved_animals=saved_animals )
      finally:
         RequestConnectionProvider.set( previous_connection )

      return ItineraryTransportationAnimalLikelihoodLookup( animals )
