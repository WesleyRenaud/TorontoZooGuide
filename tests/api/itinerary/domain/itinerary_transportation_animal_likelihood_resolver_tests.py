from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.domain.itinerary_transportation_animal_likelihood_resolver import ItineraryTransportationAnimalLikelihoodResolver
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


@pytest.fixture
def resolver_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.execute(
      """   CREATE TABLE ItineraryDate (
               ITINERARY_DATE       TEXT,
               ARRIVAL_TIME         TEXT,
               DEPARTURE_TIME       TEXT
            );
      """ )
   conn.execute(
      """   INSERT INTO ItineraryDate ( ITINERARY_DATE )
            VALUES ( '2026-06-15' );
      """ )
   conn.commit()
   yield conn
   conn.close()


def Test_Resolve_TestVisitDateAndViewableAnimal_ExpectLikelihood(
      resolver_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   def get_animals_for_saved_itinerary(
         *,
         day: int,
         month: int,
         year: int,
         saved_animals: list,
         temp: float | None = None ) -> list[ Animal ]:
      return [
         Animal(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            likelihood=80 ),
      ]

   monkeypatch.setattr(
      'api.itinerary.domain.itinerary_transportation_animal_likelihood_resolver.'
      'AnimalCoordinator.get_animals_for_saved_itinerary',
      get_animals_for_saved_itinerary )

   likelihoods = ItineraryTransportationAnimalLikelihoodResolver.resolve(
      resolver_conn,
      [ GIRAFFE_LINK ] )

   assert likelihoods.for_link( GIRAFFE_LINK ) == 80
