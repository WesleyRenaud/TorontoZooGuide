from __future__ import annotations

from api.animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from api.animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from api.models.animal import Animal


def Test_FromValues_TestEnclosureName_ExpectNormalizedTuple() -> None:
   species = 'Masai Giraffe'
   exhibit = 'Africa Savanna'
   enclosure_name = '  Outdoor Habitat  '
   key = SpeciesExhibitKeyBuilder.from_values( species, exhibit )

   result = ViewingSpotKeyBuilder.from_values( species, exhibit, enclosure_name )

   assert result == (
      key.species,
      key.exhibit,
      ViewingSpotKeyBuilder.name_from_value( enclosure_name ) )


def Test_FromAnimal_TestAnimal_ExpectViewingSpotKey() -> None:
   animal = Animal(
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name='Indoor' )

   result = ViewingSpotKeyBuilder.from_animal( animal )

   assert result == ViewingSpotKeyBuilder.from_values(
      animal.species,
      animal.exhibit,
      animal.enclosure_name )
