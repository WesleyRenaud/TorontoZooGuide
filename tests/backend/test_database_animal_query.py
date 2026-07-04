from __future__ import annotations

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from conftest import DbControllers


def test_animal_query_matches_species_not_exhibit( db: DbControllers ) -> None:
   species_matches = AnimalCoordinator.get_animals_matching_query(
      query='cheetah',
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   assert species_matches
   assert all(
      'cheetah' in ( animal.species or '' ).lower()
      for animal in species_matches
   )

   exhibit_matches = AnimalCoordinator.get_animals_matching_query(
      query='africa savanna',
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   assert exhibit_matches == []


def test_animal_query_helpers_dedupe_and_sort( db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_matching_query(
      query='african',
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   species_exhibits = [ ( animal.species, animal.exhibit ) for animal in animals ]

   assert species_exhibits == sorted(
      species_exhibits,
      key=lambda pair: ( pair[ 0 ].lower(), ( pair[ 1 ] or '' ).lower() ) )
   assert len( species_exhibits ) == len( set( species_exhibits ) )
   assert all(
      'african' in ( animal.species or '' ).lower()
      for animal in animals
   )


def test_animal_query_returns_same_species_in_multiple_exhibits( db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_matching_query(
      query='cheetah',
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   exhibits = { animal.exhibit for animal in animals if animal.species == 'Cheetah' }

   assert exhibits == { 'Africa Savanna', 'Indo-Malaya Outdoor' }


def test_basic_animal_lookup_methods( db: DbControllers ) -> None:
   assert 'African Lion' in ExhibitCoordinator.get_names_of_animals_in_exhibit( 'Africa Savanna' )

   information = AnimalCoordinator.get_animal_information(
      'African Lion',
      exhibit='Africa Savanna' )

   assert information.species == 'African Lion'
   assert information.exhibit == 'Africa Savanna'


def test_animal_information_resolves_exhibit_for_multi_exhibit_species(
      db: DbControllers,
) -> None:
   pavilion_kudu = AnimalCoordinator.get_animal_information(
      'Greater Kudu',
      exhibit='African Rainforest Pavilion' )

   assert pavilion_kudu is not None
   assert pavilion_kudu.exhibit == 'African Rainforest Pavilion'

   tundra_eagle = AnimalCoordinator.get_animal_information(
      'Northern Bald Eagle',
      exhibit='Tundra Trek' )

   assert tundra_eagle is not None
   assert tundra_eagle.exhibit == 'Tundra Trek'
   assert tundra_eagle.seasonal_viewing_summary == 'Year-round'

   domain_eagle = AnimalCoordinator.get_animal_information(
      'Northern Bald Eagle',
      exhibit='Canadian Domain' )

   assert domain_eagle is not None
   assert domain_eagle.exhibit == 'Canadian Domain'
   assert domain_eagle.seasonal_viewing_summary == 'Mar-Dec'
