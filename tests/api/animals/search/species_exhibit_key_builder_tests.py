from __future__ import annotations

from api.animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from api.models.animal import Animal


def Test_FromAnimal_TestAnimal_ExpectNormalizedKey() -> None:
   animal = Animal( species='Masai Giraffe', exhibit='Africa Savanna' )

   key = SpeciesExhibitKeyBuilder.from_animal( animal )

   assert key == SpeciesExhibitKeyBuilder.from_values( animal.species, animal.exhibit )


def Test_AnyLinkedIn_TestOverlappingKeys_ExpectTrue() -> None:
   linked = SpeciesExhibitKeyBuilder.from_values( 'African Lion', 'Africa Savanna' )
   animal_keys = [
      SpeciesExhibitKeyBuilder.from_values( 'Masai Giraffe', 'Africa Savanna' ),
      linked,
   ]
   linked_animals = [ linked ]

   result = SpeciesExhibitKeyBuilder.any_linked_in( animal_keys, linked_animals )

   assert result is True


def Test_AnyLinkedIn_TestNoOverlap_ExpectFalse() -> None:
   animal_keys = [
      SpeciesExhibitKeyBuilder.from_values( 'Masai Giraffe', 'Africa Savanna' ),
   ]
   linked_animals = [
      SpeciesExhibitKeyBuilder.from_values(
         'Western Lowland Gorilla',
         'African Rainforest Pavilion' ),
   ]

   result = SpeciesExhibitKeyBuilder.any_linked_in( animal_keys, linked_animals )

   assert result is False
