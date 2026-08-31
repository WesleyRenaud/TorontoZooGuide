from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.bulk_schedule_walk_order_builder import BulkScheduleWalkOrderBuilder
from api.walk_graph.enclosure_viewing_walk_node_lookup import EnclosureViewingWalkNodeLookup


PAVILION = 'African Rainforest Pavilion'


def test_walk_node_id_by_enclosure_name_resolves_named_and_unnamed_viewing_spots() -> None:
   walk_node_ids = EnclosureViewingWalkNodeLookup.walk_node_id_by_enclosure_name()

   assert walk_node_ids[
      ( 'Marabou Stork', PAVILION, 'Savanna Overlook' )
   ] == 'v-0263'

   assert walk_node_ids[
      ( 'Ostrich', 'Africa Savanna', None )
   ] == 'v-0426'


def test_sort_animals_for_bulk_schedule_orders_animals_by_master_route() -> None:
   animals = BulkScheduleWalkOrderBuilder.sort_animals(
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
            exhibit=PAVILION,
            enclosure_name='Savanna Overlook',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Marabou Stork',
            exhibit=PAVILION,
            enclosure_name='Savanna Overlook',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='White-Headed Vulture',
            exhibit=PAVILION,
            enclosure_name='Savanna Overlook',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
   )

   assert [ ( animal.species, animal.enclosure_name ) for animal in animals ] == [
      ( 'Marabou Stork', "Grevy's Zebra Enclosure" ),
      ( 'Marabou Stork', 'Savanna Overlook' ),
      ( 'Southern Ground Hornbill', 'Savanna Overlook' ),
      ( 'White-Headed Vulture', 'Savanna Overlook' ),
   ]


def test_sort_animals_for_bulk_schedule_orders_by_master_route() -> None:
   animals = BulkScheduleWalkOrderBuilder.sort_animals(
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
   )

   assert [ ( animal.species, animal.exhibit ) for animal in animals ] == [
      ( 'African Penguin', 'Africa Savanna' ),
      ( 'African Lion', 'Africa Savanna' ),
      ( 'Cheetah', 'Indo-Malaya Outdoor' ),
   ]
