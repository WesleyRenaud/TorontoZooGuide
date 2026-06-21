from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.itinerary.scheduling.bulk.bulk_schedule_animals import is_itinerary_animal_unscheduled
from api.itinerary.scheduling.bulk.bulk_schedule_walk_order import sort_animals_for_bulk_schedule
from api.walk_graph.data_access.load_walk_graph import load_walk_graph


def test_sort_animals_for_bulk_schedule_orders_by_walk_distance_from_entrance() -> None:
   graph = load_walk_graph()
   animals = sort_animals_for_bulk_schedule(
      graph,
      [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Indo-Malaya Outdoor',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
      start_node_id=str( graph[ 'entrance_node_id' ] ) )

   assert [ ( animal.species, animal.exhibit ) for animal in animals ] == [
      ( 'Cheetah', 'Indo-Malaya Outdoor' ),
      ( 'African Penguin', 'Africa Savanna' ),
      ( 'African Lion', 'Africa Savanna' ),
   ]


def test_is_itinerary_animal_unscheduled() -> None:
   assert is_itinerary_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
      )
   )
   assert is_itinerary_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
         start_time='',
         end_time='',
      )
   )
   assert not is_itinerary_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
         start_time='09:30',
         end_time='09:38',
      )
   )
   assert not has_itinerary_schedule_times( '09:30', None )
   assert not has_itinerary_schedule_times( None, '09:38' )
