from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_animal_save_carryover import itinerary_animal_save_carryover
from api.itinerary.validation.itinerary_validation import validate_itinerary_animals
from conftest import DbControllers


def test_validate_animals_removes_unavailable_entries(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   AnimalCoordinator.set_animal_as_off_display(
      species='African Lion',
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Unavailable.'
   )

   result = validate_itinerary_animals(
      AnimalCoordinator,
      animals=[
         ItineraryAnimalInput(
            species='African Lion',
            exhibit='Africa Savanna' ),
         ItineraryAnimalInput(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor' ),
      ],
      new_visit_date=date( 2026, 6, 15 ),
      arrival_time='09:30',
      departure_time='17:00',
      new_visit_date_temp=22,
      old_visit_date='2026-06-15' )

   assert len( result ) == 2

   assert [
      ( d.species, ( d.new_likelihood or 0 ) > 0 )
      for d in result
      if d.species == 'African Lion'
   ] == [ ( 'African Lion', False ) ]

   assert [
      ( d.species, ( d.new_likelihood or 0 ) > 0 )
      for d in result
      if d.species == 'African Penguin'
   ] == [ ( 'African Penguin', True ) ]


def test_get_itinerary_animals_keeps_indoor_and_outdoor_viewing_for_map_markers(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 5, 30 ) )

   animals = AnimalCoordinator.get_animals_for_saved_itinerary(
      day=30,
      month='May',
      year=2026,
      saved_animals=[
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Giraffe House',
            old_likelihood=100,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            old_likelihood=100,
            new_likelihood=100,
         ),
      ],
   )

   giraffes = [
      animal
      for animal in animals
      if animal.species == 'Masai Giraffe'
   ]

   assert sorted( [
      ( giraffe.exhibit, giraffe.enclosure_type, giraffe.x_coord, giraffe.y_coord )
      for giraffe in giraffes
   ] ) == [
      ( 'Africa Savanna', 'Indoor', 42.35, 71.366 ),
      ( 'Africa Savanna', 'Outdoor', 39.885, 70.927 ),
   ]
   assert all( giraffe.likelihood == 100 for giraffe in giraffes )
   assert all( giraffe.old_likelihood == 100 for giraffe in giraffes )


def test_validate_animals_resolves_likelihood_for_viewing_spot(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 5, 26 ) )

   result = validate_itinerary_animals(
      AnimalCoordinator,
      animals=[
         ItineraryAnimalInput(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Giraffe House' ),
      ],
      new_visit_date=date( 2026, 5, 30 ),
      arrival_time='09:30',
      departure_time='17:00',
      old_visit_date='2026-05-26',
      saved_animal_rows=[
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Giraffe House',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
   )

   assert [ ( d.species, d.new_likelihood ) for d in result ] == [
      ( 'Masai Giraffe', 100 )
   ]


def test_itinerary_animal_save_carryover_matches_species_exhibit_case_insensitively() -> None:
   carryover = itinerary_animal_save_carryover(
      [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='2:30 PM',
            end_time='2:45 PM',
         ),
      ],
      ItineraryAnimalInput(
         species='African Lion',
         exhibit='Africa Savanna' ),
      old_visit_date='2026-06-15',
   )

   assert carryover.start_time == '2:30 PM'
   assert carryover.end_time == '2:45 PM'
