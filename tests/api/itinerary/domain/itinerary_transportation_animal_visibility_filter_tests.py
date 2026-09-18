from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_transportation_animal_visibility_filter import ItineraryTransportationAnimalVisibilityFilter
from api.models.animal import Animal
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.transportation.data_access.transportation_animal_provider import TransportationAnimalProvider
from api.transportation.data_access.transportation_animal_record import TransportationAnimalRecord


def _animal(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str,
      added_by_transportation: bool = False ) -> Animal:
   return Animal(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      added_by_transportation=added_by_transportation )


def _leg(
      *,
      from_station: str,
      to_station: str,
      start_time: str,
      end_time: str ) -> ItineraryTransportationLeg:
   return ItineraryTransportationLeg(
      from_station=from_station,
      to_station=to_station,
      start_time=start_time,
      end_time=end_time,
      transportation='Zoomobile',
      added_as_attraction=False )


GIRAFFE_LINK = TransportationAnimalRecord(
   transportation='Zoomobile',
   from_station='Canadian Domain Zoomobile Station',
   to_station='Africa Zoomobile Station',
   species='Masai Giraffe',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)

ZEBRA_LINK = TransportationAnimalRecord(
   transportation='Zoomobile',
   from_station='Main Zoomobile Station',
   to_station='Canadian Domain Zoomobile Station',
   species="Grevy's Zebra",
   exhibit='Canadian Domain',
   enclosure_name='Savanna Grasslands',
)


def Test_Apply_TestNoTransportationAnimals_ExpectUnchanged() -> None:
   lion = _animal(
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )

   animals = ItineraryTransportationAnimalVisibilityFilter.apply(
      [ lion ],
      itinerary_legs=[] )

   assert animals == [ lion ]


def Test_Apply_TestMatchingHop_ExpectTransportationAnimalKept(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   giraffe = _animal(
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
      added_by_transportation=True )
   lion = _animal(
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )
   monkeypatch.setattr(
      TransportationAnimalProvider,
      'fetch_all',
      lambda conn: [ GIRAFFE_LINK ] )

   animals = ItineraryTransportationAnimalVisibilityFilter.apply(
      [ giraffe, lion ],
      itinerary_legs=[
         _leg(
            from_station='Canadian Domain Zoomobile Station',
            to_station='Africa Zoomobile Station',
            start_time='10:20 AM',
            end_time='10:30 AM' ),
      ] )

   assert animals == [ giraffe, lion ]


def Test_Apply_TestMissingHop_ExpectTransportationAnimalHidden(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   giraffe = _animal(
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
      added_by_transportation=True )
   lion = _animal(
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )
   monkeypatch.setattr(
      TransportationAnimalProvider,
      'fetch_all',
      lambda conn: [ GIRAFFE_LINK ] )

   animals = ItineraryTransportationAnimalVisibilityFilter.apply(
      [ giraffe, lion ],
      itinerary_legs=[] )

   assert animals == [ lion ]


def Test_Apply_TestUnknownCatalogSpot_ExpectTransportationAnimalHidden(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   giraffe = _animal(
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
      added_by_transportation=True )
   monkeypatch.setattr(
      TransportationAnimalProvider,
      'fetch_all',
      lambda conn: [ ZEBRA_LINK ] )

   animals = ItineraryTransportationAnimalVisibilityFilter.apply(
      [ giraffe ],
      itinerary_legs=[
         _leg(
            from_station='Canadian Domain Zoomobile Station',
            to_station='Africa Zoomobile Station',
            start_time='10:20 AM',
            end_time='10:30 AM' ),
      ] )

   assert animals == []
