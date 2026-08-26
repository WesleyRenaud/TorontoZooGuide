from __future__ import annotations

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.itinerary.itinerary_animals_builder import ItineraryAnimalsBuilder
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def test_itinerary_filter_helpers_sort_matching_animals( db: DbControllers ) -> None:
   animal_controller = AnimalCoordinator
   attraction_coordinator = AttractionCoordinator

   animals = animal_controller.get_animals_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_animals=[
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=None ),
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=None ),
      ] )
   attractions = attraction_coordinator.get_attractions_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_attractions=[
         ItineraryAttractionRecord(
            attraction='Greenhouse',
            old_likelihood=None,
            new_likelihood=None ),
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=None ),
      ] )

   assert [ animal.species for animal in animals ] == sorted(
      [ animal.species for animal in animals ],
      key=str.lower
   )
   assert { animal.species for animal in animals } == { 'African Lion', 'African Penguin' }
   assert [ attraction.name for attraction in attractions ] == [ 'Conservation Carousel', 'Greenhouse' ]


def test_itinerary_animals_keep_same_species_in_multiple_exhibits_for_map_markers(
      db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_animals=[
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=None ),
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Indo-Malaya Outdoor',
            old_likelihood=None,
            new_likelihood=None ),
      ] )

   assert [
      ( animal.species, animal.exhibit )
      for animal in animals
      if animal.species == 'Cheetah'
   ] == [
      ( 'Cheetah', 'Africa Savanna' ),
      ( 'Cheetah', 'Indo-Malaya Outdoor' ),
   ]


def test_itinerary_filter_helpers_return_empty_without_filters( db: DbControllers ) -> None:
   assert ItineraryAnimalsBuilder.build( [], [] ) == []
   assert AnimalCoordinator.get_animals_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_animals=[],
   ) == []
   assert AttractionCoordinator.get_attractions_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_attractions=[],
   ) == []
   assert GuardiansCoordinator.get_guardians_talk_details(
      guardians_talks_to_include=[]
   ) == []
   assert WildEncounterCoordinator.get_wild_encounter_details(
      wild_encounters_to_include=[]
   ) == []
