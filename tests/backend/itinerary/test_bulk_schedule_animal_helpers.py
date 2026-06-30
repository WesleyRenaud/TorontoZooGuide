from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.itinerary.scheduling.bulk.bulk_schedule_animals import is_itinerary_animal_unscheduled
from api.itinerary.scheduling.bulk.bulk_schedule_walk_order import sort_animals_for_bulk_schedule
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.enclosure_viewing_walk_node_lookup import walk_node_id_by_enclosure_name


def test_walk_node_id_by_enclosure_name_resolves_named_and_unnamed_viewing_spots() -> None:
   walk_node_ids = walk_node_id_by_enclosure_name()

   assert walk_node_ids[
      ( 'Marabou Stork', 'Africa Savanna', 'Savanna Overlook' )
   ] == 'v-0263'

   assert walk_node_ids[
      ( 'Ostrich', 'Africa Savanna', None )
   ] == 'v-0426'


def test_sort_animals_for_bulk_schedule_groups_animals_at_the_same_viewing_spot() -> None:
   graph = load_walk_graph()
   animals = sort_animals_for_bulk_schedule(
      graph,
      [
         ItineraryAnimalRecord(
            species='Marabou Stork',
            exhibit='Africa Savanna',
            enclosure_name="Grevy's Zebra Enclosure",
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Southern Ground Hornbill',
            exhibit='Africa Savanna',
            enclosure_name='Savanna Overlook',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Marabou Stork',
            exhibit='Africa Savanna',
            enclosure_name='Savanna Overlook',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='White-Headed Vulture',
            exhibit='Africa Savanna',
            enclosure_name='Savanna Overlook',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
      start_node_id='v-0263',
   )

   assert [ animal.enclosure_name for animal in animals[ :3 ] ] == [
      'Savanna Overlook',
      'Savanna Overlook',
      'Savanna Overlook',
   ]
   assert animals[ 3 ].enclosure_name == "Grevy's Zebra Enclosure"


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
            enclosure_name='Outdoor',
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
