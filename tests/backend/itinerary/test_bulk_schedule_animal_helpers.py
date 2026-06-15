from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.itinerary.scheduling.bulk.bulk_schedule_animals import is_itinerary_animal_unscheduled
from api.itinerary.scheduling.bulk.bulk_schedule_animals import sort_animals_for_bulk_schedule
from api.itinerary.scheduling.bulk.bulk_schedule_exhibit_order import bulk_schedule_exhibit_rank


def test_sort_animals_for_bulk_schedule_orders_by_exhibit_then_species() -> None:
   animals = sort_animals_for_bulk_schedule( [
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
   ] )

   assert [ ( animal.species, animal.exhibit ) for animal in animals ] == [
      ( 'Cheetah', 'Indo-Malaya Outdoor' ),
      ( 'African Lion', 'Africa Savanna' ),
      ( 'African Penguin', 'Africa Savanna' ),
   ]


def test_bulk_schedule_exhibit_rank_orders_americas_pavilion_before_mayan_temple() -> None:
   assert bulk_schedule_exhibit_rank( 'Americas Pavilion' ) < bulk_schedule_exhibit_rank(
      'Americas Outdoor Mayan Temple Ruins' )


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
