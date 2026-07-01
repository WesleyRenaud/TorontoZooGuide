from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.bulk_schedule_walk_order import sort_animals_for_bulk_schedule
from api.walk_graph.data_access.load_walk_graph import load_walk_graph


def test_sort_animals_for_bulk_schedule_visits_canadian_domain_before_deeper_savanna() -> None:
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
            species='Spotted Hyena',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Watusi Cattle',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            enclosure_name='Male Herd',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Grizzly Bear',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
      start_node_id=str( graph[ 'entrance_node_id' ] ) )

   species_order = [ animal.species for animal in animals ]
   lion_index = species_order.index( 'African Lion' )
   bison_index = species_order.index( 'Wood Bison' )
   grizzly_index = species_order.index( 'Grizzly Bear' )
   watusi_index = species_order.index( 'Watusi Cattle' )

   assert bison_index < lion_index
   assert grizzly_index < lion_index
   assert watusi_index < bison_index
