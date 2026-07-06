from __future__ import annotations

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from conftest import DbControllers


def _viewing_spots_for_species(
      animals: list,
      *,
      species: str,
      exhibit: str ) -> list[ tuple[ str | None, str | None ] ]:
   return sorted(
      (
         animal.enclosure_type,
         animal.enclosure_name,
      )
      for animal in animals
      if animal.species == species and animal.exhibit == exhibit )


def test_giraffe_excludes_indoor_viewing_when_outdoor_is_likely(
      db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      exhibits_to_include=[ 'Africa Savanna' ] )

   assert _viewing_spots_for_species(
      animals,
      species='Masai Giraffe',
      exhibit='Africa Savanna' ) == [
      ( 'Outdoor', 'Outdoor' ),
   ]


def test_giraffe_includes_indoor_viewing_when_outdoor_is_unlikely(
      db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='January',
      year=2026,
      temp=-5,
      exhibits_to_include=[ 'Africa Savanna' ] )

   assert _viewing_spots_for_species(
      animals,
      species='Masai Giraffe',
      exhibit='Africa Savanna' ) == [
      ( 'Indoor', 'Giraffe House' ),
   ]

   giraffe = next(
      animal
      for animal in animals
      if animal.species == 'Masai Giraffe' )

   assert giraffe.likelihood == 100


def test_giraffe_adds_alternate_habitat_alert_when_outdoor_likelihood_is_partial(
      db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=12,
      exhibits_to_include=[ 'Africa Savanna' ] )

   giraffe = next(
      animal
      for animal in animals
      if animal.species == 'Masai Giraffe' )

   assert giraffe.enclosure_type == 'Outdoor'
   assert giraffe.likelihood == 84
   assert giraffe.has_viewing_alert is True
   assert giraffe.viewing_alert_messages == [
      'If you do not see the Masai Giraffe outside, '
      'then check their indoor habitat.',
   ]


def test_giraffe_excludes_alternate_habitat_alert_when_outdoor_is_certain(
      db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      exhibits_to_include=[ 'Africa Savanna' ] )

   giraffe = next(
      animal
      for animal in animals
      if animal.species == 'Masai Giraffe' )

   assert giraffe.enclosure_type == 'Outdoor'
   assert giraffe.likelihood == 100
   assert giraffe.has_viewing_alert is False
   assert giraffe.viewing_alert_messages == []


def test_gorilla_includes_indoor_and_outdoor_when_outdoor_is_likely(
      db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      exhibits_to_include=[ 'African Rainforest Pavilion' ] )

   assert { animal.enclosure_type for animal in animals
            if animal.species == 'Western Lowland Gorilla' } == {
      'Indoor',
      'Outdoor',
   }


def test_rhino_excludes_indoor_viewing_when_outdoor_is_likely(
      db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      exhibits_to_include=[ 'Indo-Malaya Outdoor' ] )

   assert _viewing_spots_for_species(
      animals,
      species='Greater One-Horned Rhinoceros',
      exhibit='Indo-Malaya Outdoor' ) == [
      ( 'Outdoor', 'Outdoor' ),
   ]
