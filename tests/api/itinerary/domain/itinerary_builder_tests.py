from __future__ import annotations

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.domain.itinerary_transportation_stations_builder import ItineraryTransportationStationsBuilder
from api.itinerary.domain.itinerary_transportations_builder import ItineraryTransportationsBuilder
from api.models.animal import Animal
from api.models.attraction import Attraction
from api.models.guardians_talk import GuardiansTalk
from api.models.wild_encounter import WildEncounter
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animal_rows=[
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
      ),
   ],
   attraction_rows=[
      ItineraryAttractionRecord(
         attraction='Conservation Carousel',
         old_likelihood=None,
         new_likelihood=100,
      ),
   ],
   guardians_talk_rows=[
      ItineraryGuardiansTalkRecord(
         talk_name='African Lion',
         start_time='10:00 AM',
         end_time='10:30 AM',
         is_deleted=False,
      ),
   ],
   wild_encounter_rows=[
      ItineraryWildEncounterRecord(
         wild_encounter='African Rainforest',
         start_time='2:00 PM',
         end_time='2:45 PM',
         is_deleted=False,
      ),
   ],
)


@pytest.fixture
def stub_itinerary_builder_coordinators(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      lambda **kwargs: [
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            likelihood=100,
            old_likelihood=None ),
      ] )
   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attractions_for_saved_itinerary',
      lambda **kwargs: [
         Attraction(
            name='Conservation Carousel',
            free_with_admission=0,
            likelihood=100,
            old_likelihood=None ),
      ] )
   monkeypatch.setattr(
      GuardiansCoordinator,
      'get_guardians_talks_for_saved_itinerary',
      lambda rows: [
         GuardiansTalk(
            name='African Lion',
            location='Africa Savanna',
            x_coord=0.0,
            y_coord=0.0,
            start_time='10:00 AM',
            end_time='10:30 AM' ),
      ] )
   monkeypatch.setattr(
      WildEncounterCoordinator,
      'get_wild_encounters_for_saved_itinerary',
      lambda rows: [
         WildEncounter(
            name='African Rainforest',
            meeting_spot='Rainforest Gate',
            link='african-rainforest',
            x_coord=0.0,
            y_coord=0.0,
            start_time='2:00 PM',
            end_time='2:45 PM' ),
      ] )
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

   assert itinerary.date == '2026-06-15'
   assert itinerary.arrival_time == '9:30 AM'
   assert itinerary.departure_time == '5:00 PM'
   assert [ animal.species for animal in itinerary.animals ] == [ 'African Lion' ]
   assert [ attraction.name for attraction in itinerary.attractions ] == [
      'Conservation Carousel',
   ]
   assert [
      ( talk.name, talk.start_time, talk.end_time )
      for talk in itinerary.guardians_talks
   ] == [
      ( 'African Lion', '10:00 AM', '10:30 AM' ),
   ]
   assert [
      ( encounter.name, encounter.start_time, encounter.end_time )
      for encounter in itinerary.wild_encounters
   ] == [
      ( 'African Rainforest', '2:00 PM', '2:45 PM' ),
   ]

   itinerary_dict = itinerary.to_dict()
   assert itinerary_dict[ 'animals' ][ 0 ][ 'old_likelihood' ] is None
   assert itinerary_dict[ 'animals' ][ 0 ][ 'likelihood' ] > 0
   assert itinerary_dict[ 'attractions' ][ 0 ][ 'old_likelihood' ] is None
   assert itinerary_dict[ 'attractions' ][ 0 ][ 'likelihood' ] > 0


def Test_BuildCurrent_TestEmptySavedItinerary_ExpectEmpty(
      stub_itinerary_builder_coordinators: None ) -> None:
   itinerary = ItineraryBuilder.build_current(
      SavedItinerary(
         date_value=None,
         arrival_time=None,
         departure_time=None,
      ),
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert itinerary.date == ''
   assert itinerary.animals == []
   assert itinerary.attractions == []
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []
