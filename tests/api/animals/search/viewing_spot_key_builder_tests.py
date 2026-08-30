from __future__ import annotations

from api.animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from api.models.animal import Animal


def Test_FromValues_TestEnclosureName_ExpectNormalizedTuple() -> None:
   species, exhibit, enclosure_name = ViewingSpotKeyBuilder.from_values(
      'Masai Giraffe',
      'Africa Savanna',
      '  Outdoor Habitat  ' )

   assert species == 'masai giraffe'
   assert exhibit == 'africa savanna'
   assert enclosure_name == 'Outdoor Habitat'


def Test_FromAnimal_TestAnimal_ExpectViewingSpotKey() -> None:
   animal = Animal(
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name='Indoor' )

   assert ViewingSpotKeyBuilder.from_animal( animal ) == (
      'african lion',
      'africa savanna',
      'Indoor',
   )
