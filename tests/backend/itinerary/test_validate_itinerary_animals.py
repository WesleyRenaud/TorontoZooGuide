from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from conftest import DbControllers


def test_get_itinerary_animals_keeps_indoor_and_outdoor_viewing_for_map_markers(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 5, 30 ) )

   animals = AnimalCoordinator.get_animals_for_saved_itinerary(
      day=30,
      month='May',
      year=2026,
      temp=22,
      saved_animals=[
         ItineraryAnimalRecord(
            species='Western Lowland Gorilla',
            exhibit='African Rainforest Pavilion',
            enclosure_name='Indoor',
            old_likelihood=100,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Western Lowland Gorilla',
            exhibit='African Rainforest Pavilion',
            enclosure_name='Outdoor',
            old_likelihood=100,
            new_likelihood=100,
         ),
      ],
   )

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
