from __future__ import annotations

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.domain.itinerary_transportation_stations_builder import ItineraryTransportationStationsBuilder
from api.itinerary.domain.itinerary_transportations_builder import ItineraryTransportationsBuilder
from api.models.animal import Animal
from api.models.attraction import Attraction
from api.models.guardians_talk import GuardiansTalk
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.models.wild_encounter import WildEncounter
from api.shared.enums.position import Position
from api.transportation.data_access.transportation_animal_provider import TransportationAnimalProvider
from api.transportation.data_access.transportation_animal_record import TransportationAnimalRecord
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   likelihood=100,
   old_likelihood=None )
CAROUSEL = Attraction(
   name='Conservation Carousel',
   free_with_admission=0,
   likelihood=100,
   old_likelihood=None )
LION_TALK = GuardiansTalk(
   name='African Lion',
   location='Africa Savanna',
   x_coord=0.0,
   y_coord=0.0,
   start_time='10:00 AM',
   end_time='10:30 AM' )
RAINFOREST = WildEncounter(
   name='African Rainforest',
   meeting_spot='Rainforest Gate',
   link='african-rainforest',
   x_coord=0.0,
   y_coord=0.0,
   start_time='2:00 PM',
   end_time='2:45 PM' )
SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animal_rows=[
      ItineraryAnimalRecord(
         species=LION.species,
         exhibit=LION.exhibit,
         old_likelihood=LION.old_likelihood,
         new_likelihood=LION.likelihood,
      ),
   ],
   attraction_rows=[
      ItineraryAttractionRecord(
         attraction=CAROUSEL.name,
         old_likelihood=CAROUSEL.old_likelihood,
         new_likelihood=CAROUSEL.likelihood,
      ),
   ],
   guardians_talk_rows=[
      ItineraryGuardiansTalkRecord(
         talk_name=LION_TALK.name,
         start_time=LION_TALK.start_time,
         end_time=LION_TALK.end_time,
         is_deleted=False,
      ),
   ],
   wild_encounter_rows=[
      ItineraryWildEncounterRecord(
         wild_encounter=RAINFOREST.name,
         start_time=RAINFOREST.start_time,
         end_time=RAINFOREST.end_time,
         is_deleted=False,
      ),
   ],
)
GIRAFFE_LINK = TransportationAnimalRecord(
   transportation='Zoomobile',
   from_station='Canadian Domain Zoomobile Station',
   to_station='Africa Zoomobile Station',
   species='Masai Giraffe',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor' )


@pytest.fixture
def stub_itinerary_builder_coordinators(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      lambda **kwargs: [ LION ] )
   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attractions_for_saved_itinerary',
      lambda **kwargs: [ CAROUSEL ] )
   monkeypatch.setattr(
      GuardiansCoordinator,
      'get_guardians_talks_for_saved_itinerary',
      lambda rows: [ LION_TALK ] )
   monkeypatch.setattr(
      WildEncounterCoordinator,
      'get_wild_encounters_for_saved_itinerary',
      lambda rows: [ RAINFOREST ] )
   monkeypatch.setattr(
      ItineraryTransportationsBuilder,
      'build',
      lambda saved_transportations, target_date: [] )
   monkeypatch.setattr(
      ItineraryTransportationStationsBuilder,
      'attach_to_transportations',
      lambda transportations: [] )


def Test_BuildCurrent_TestSavedItinerary_ExpectAssembledGuestContent(
      stub_itinerary_builder_coordinators: None ) -> None:
   itinerary = ItineraryBuilder.build_current(
      SAVED_ITINERARY,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert itinerary.date == SAVED_ITINERARY.date_value
   assert itinerary.arrival_time == SAVED_ITINERARY.arrival_time
   assert itinerary.departure_time == SAVED_ITINERARY.departure_time
   assert itinerary.animals == [ LION ]
   assert itinerary.attractions == [ CAROUSEL ]
   assert itinerary.guardians_talks == [ LION_TALK ]
   assert itinerary.wild_encounters == [ RAINFOREST ]


def Test_BuildCurrent_TestSavedItinerary_ExpectLikelihoodsInDict(
      stub_itinerary_builder_coordinators: None ) -> None:
   itinerary = ItineraryBuilder.build_current(
      SAVED_ITINERARY,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   itinerary_dict = itinerary.to_dict()

   animal = itinerary_dict[ 'animals' ][ Position.FIRST ]
   attraction = itinerary_dict[ 'attractions' ][ Position.FIRST ]

   assert animal[ 'old_likelihood' ] is LION.old_likelihood
   assert animal[ 'likelihood' ] == LION.likelihood
   assert attraction[ 'old_likelihood' ] is CAROUSEL.old_likelihood
   assert attraction[ 'likelihood' ] == CAROUSEL.likelihood


def Test_BuildCurrent_TestEmptySavedItinerary_ExpectEmpty(
      stub_itinerary_builder_coordinators: None ) -> None:
   saved = SavedItinerary(
      date_value=None,
      arrival_time=None,
      departure_time=None,
   )
   empty = ItineraryBuilder.empty()

   itinerary = ItineraryBuilder.build_current(
      saved,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert itinerary.date == empty.date
   assert itinerary.animals == empty.animals
   assert itinerary.attractions == empty.attractions
   assert itinerary.guardians_talks == empty.guardians_talks
   assert itinerary.wild_encounters == empty.wild_encounters


def Test_BuildCurrent_TestTransportationAnimal_ExpectCatalogApplied(
      stub_itinerary_builder_coordinators: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   giraffe = Animal(
      species=GIRAFFE_LINK.species,
      exhibit=GIRAFFE_LINK.exhibit,
      enclosure_name=GIRAFFE_LINK.enclosure_name,
      added_by_transportation=True,
      transportation=GIRAFFE_LINK.transportation )
   matching_leg = ItineraryTransportationLeg(
      from_station=GIRAFFE_LINK.from_station,
      to_station=GIRAFFE_LINK.to_station,
      start_time='10:20 AM',
      end_time='10:30 AM',
      transportation=GIRAFFE_LINK.transportation,
      added_as_attraction=False )
   saved = SavedItinerary(
      date_value=SAVED_ITINERARY.date_value,
      arrival_time=SAVED_ITINERARY.arrival_time,
      departure_time=SAVED_ITINERARY.departure_time,
      animal_rows=[
         ItineraryAnimalRecord(
            species=giraffe.species,
            exhibit=giraffe.exhibit,
            enclosure_name=giraffe.enclosure_name,
            added_by_transportation=True ),
      ],
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation=GIRAFFE_LINK.transportation,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False,
            start_time=matching_leg.start_time,
            end_time=matching_leg.end_time,
            legs=[ matching_leg ] ),
      ],
   )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      lambda **kwargs: [ giraffe ] )
   monkeypatch.setattr(
      TransportationAnimalProvider,
      'fetch_all',
      lambda conn: [ GIRAFFE_LINK ] )

   itinerary = ItineraryBuilder.build_current(
      saved,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert itinerary.animals == [ giraffe ]
   assert giraffe.transportation == GIRAFFE_LINK.transportation
