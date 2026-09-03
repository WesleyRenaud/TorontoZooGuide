from __future__ import annotations

from api.animals.itinerary.itinerary_animals_builder import ItineraryAnimalsBuilder
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.models.animal import Animal


def _animal(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None,
      enclosure_type: str | None = None,
      x_coord: float | None = None,
      y_coord: float | None = None,
      likelihood: int | None = None ) -> Animal:
   return Animal(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      enclosure_type=enclosure_type,
      x_coord=x_coord,
      y_coord=y_coord,
      likelihood=likelihood )


def _saved_animal(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None,
      old_likelihood: int | None = None,
      is_added: bool = False,
      covered_by_talk: bool = False,
      start_time: str | None = None,
      end_time: str | None = None ) -> ItineraryAnimalRecord:
   return ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      old_likelihood=old_likelihood,
      new_likelihood=old_likelihood,
      is_added=is_added,
      covered_by_talk=covered_by_talk,
      start_time=start_time,
      end_time=end_time )


def Test_Build_TestEmptyInputs_ExpectEmpty() -> None:
   assert ItineraryAnimalsBuilder.build( [], [] ) == []


def Test_Build_TestFiltersToSavedSpots_ExpectOnlyMatchingAnimals() -> None:
   viewable_animals = [
      _animal( species='African Lion', exhibit='Africa Savanna' ),
      _animal( species='African Penguin', exhibit='Africa Savanna', enclosure_name='Outdoor' ),
      _animal( species='Masai Giraffe', exhibit='Africa Savanna' ),
   ]
   saved_animals = [
      _saved_animal(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor' ),
      _saved_animal(
         species='African Lion',
         exhibit='Africa Savanna' ),
   ]

   animals = ItineraryAnimalsBuilder.build( viewable_animals, saved_animals )

   assert { animal.species for animal in animals } == { 'African Lion', 'African Penguin' }


def Test_Build_TestSortsBySpecies_ExpectSortedOrder() -> None:
   viewable_animals = [
      _animal( species='African Penguin', exhibit='Africa Savanna', enclosure_name='Outdoor' ),
      _animal( species='African Lion', exhibit='Africa Savanna' ),
   ]
   saved_animals = [
      _saved_animal(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor' ),
      _saved_animal(
         species='African Lion',
         exhibit='Africa Savanna' ),
   ]

   animals = ItineraryAnimalsBuilder.build( viewable_animals, saved_animals )

   assert [ animal.species for animal in animals ] == sorted(
      [ animal.species for animal in animals ],
      key=str.lower,
   )


def Test_Build_TestSameSpeciesMultipleExhibits_ExpectBothRows() -> None:
   viewable_animals = [
      _animal( species='Cheetah', exhibit='Africa Savanna' ),
      _animal( species='Cheetah', exhibit='Indo-Malaya Outdoor' ),
      _animal( species='African Lion', exhibit='Africa Savanna' ),
   ]
   saved_animals = [
      _saved_animal( species='Cheetah', exhibit='Africa Savanna' ),
      _saved_animal( species='Cheetah', exhibit='Indo-Malaya Outdoor' ),
   ]

   animals = ItineraryAnimalsBuilder.build( viewable_animals, saved_animals )

   assert [
      ( animal.species, animal.exhibit )
      for animal in animals
      if animal.species == 'Cheetah'
   ] == [
      ( 'Cheetah', 'Africa Savanna' ),
      ( 'Cheetah', 'Indo-Malaya Outdoor' ),
   ]


def Test_Build_TestIndoorAndOutdoorGorillas_ExpectBothSpots() -> None:
   viewable_animals = [
      _animal(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         enclosure_name='Indoor',
         enclosure_type='Indoor',
         x_coord=47.487,
         y_coord=62.703,
         likelihood=100 ),
      _animal(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         enclosure_name='Outdoor',
         enclosure_type='Outdoor',
         x_coord=48.951,
         y_coord=59.856,
         likelihood=100 ),
      _animal( species='African Lion', exhibit='Africa Savanna' ),
   ]
   saved_animals = [
      _saved_animal(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         enclosure_name='Indoor',
         old_likelihood=100 ),
      _saved_animal(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         enclosure_name='Outdoor',
         old_likelihood=100 ),
   ]

   animals = ItineraryAnimalsBuilder.build( viewable_animals, saved_animals )

   gorillas = [
      animal
      for animal in animals
      if animal.species == 'Western Lowland Gorilla'
   ]

   assert sorted( [
      ( gorilla.exhibit, gorilla.enclosure_type, gorilla.x_coord, gorilla.y_coord )
      for gorilla in gorillas
   ] ) == [
      ( 'African Rainforest Pavilion', 'Indoor', 47.487, 62.703 ),
      ( 'African Rainforest Pavilion', 'Outdoor', 48.951, 59.856 ),
   ]
   assert all( gorilla.likelihood == 100 for gorilla in gorillas )
   assert all( gorilla.old_likelihood == 100 for gorilla in gorillas )


def Test_Build_TestAppliesSavedSchedule_ExpectTimesAndFlags() -> None:
   viewable_animals = [
      _animal( species='African Lion', exhibit='Africa Savanna' ),
   ]
   saved_animals = [
      _saved_animal(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=80,
         is_added=True,
         covered_by_talk=True,
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]

   animals = ItineraryAnimalsBuilder.build( viewable_animals, saved_animals )

   lion = animals[ 0 ]
   assert lion.old_likelihood == 80
   assert lion.is_added is True
   assert lion.covered_by_talk is True
   assert lion.start_time == '10:00 AM'
   assert lion.end_time == '10:08 AM'


def Test_FindSavedAnimalForViewableAnimal_TestNoMatch_ExpectNone() -> None:
   animal = _animal( species='African Lion', exhibit='Africa Savanna' )

   assert ItineraryAnimalsBuilder._find_saved_animal_for_viewable_animal( [], animal ) is None


def Test_ApplyOldLikelihood_TestNoSavedMatch_ExpectUnchanged() -> None:
   animal = _animal( species='African Lion', exhibit='Africa Savanna' )

   ItineraryAnimalsBuilder._apply_old_likelihood( [ animal ], [] )

   assert animal.old_likelihood is None


def Test_ApplyIsAdded_TestNoSavedMatch_ExpectUnchanged() -> None:
   animal = _animal( species='African Lion', exhibit='Africa Savanna' )

   ItineraryAnimalsBuilder._apply_is_added( [ animal ], [] )

   assert animal.is_added is False


def Test_ApplySchedule_TestNoSavedMatch_ExpectUnchanged() -> None:
   animal = _animal( species='African Lion', exhibit='Africa Savanna' )

   ItineraryAnimalsBuilder._apply_schedule( [ animal ], [] )

   assert animal.start_time is None
   assert animal.end_time is None
   assert animal.covered_by_talk is False
