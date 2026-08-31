from __future__ import annotations

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.models.animal import Animal


VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026


def _animal(
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> Animal:
   return Animal(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name )


def Test_GetAnimalsForSavedItinerary_TestEmptySavedAnimals_ExpectEmpty() -> None:
   assert AnimalCoordinator.get_animals_for_saved_itinerary(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      saved_animals=[],
   ) == []


def Test_GetAnimalsForSavedItinerary_TestSavedAnimals_ExpectBuilderFilteredAnimals(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   viewable_animals = [
      _animal( 'African Penguin', 'Africa Savanna', enclosure_name='Outdoor' ),
      _animal( 'African Lion', 'Africa Savanna' ),
      _animal( 'Masai Giraffe', 'Africa Savanna' ),
   ]
   captured: dict[ str, object ] = {}

   def get_animals_viewable_on_day( **kwargs: object ) -> list[ Animal ]:
      captured[ 'kwargs' ] = kwargs
      return viewable_animals

   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      get_animals_viewable_on_day )

   saved_animals = [
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
   ]

   animals = AnimalCoordinator.get_animals_for_saved_itinerary(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      saved_animals=saved_animals,
   )

   assert captured[ 'kwargs' ] == {
      'day': VISIT_DAY,
      'month': VISIT_MONTH,
      'year': VISIT_YEAR,
      'temp': None,
      'include_off_display_animals': True,
      'threshold': 0,
      'exhibits_to_include': [ 'Africa Savanna' ],
   }
   assert [ animal.species for animal in animals ] == [ 'African Lion', 'African Penguin' ]
