from __future__ import annotations

from ...models import Animal
from ..search.animals_matching_query import species_exhibit_key
from ...shared.constants import OUTDOOR_LIKELIHOOD_EXCLUDE_INDOOR_THRESHOLD
from ...shared.enums import EnclosureType


def should_exclude_indoor_viewing_spot(
      animal: Animal,
      *,
      outdoor_likelihood: int ) -> bool:
   return (
      animal.always_include_indoor_viewing is False
      and outdoor_likelihood >= OUTDOOR_LIKELIHOOD_EXCLUDE_INDOOR_THRESHOLD )


def apply_indoor_outdoor_viewing_visibility(
      animals: list[ Animal ] ) -> list[ Animal ]:
   outdoor_likelihood_by_species_exhibit: dict[ tuple[ str, str ], int ] = {}

   for animal in animals:
      if not EnclosureType.is_outdoor( animal.enclosure_type ):
         continue

      key = species_exhibit_key( animal )
      outdoor_likelihood_by_species_exhibit[ key ] = max(
         outdoor_likelihood_by_species_exhibit.get( key, 0 ),
         animal.likelihood or 0 )

   visible_animals: list[ Animal ] = []

   for animal in animals:
      if (
            EnclosureType.is_indoor( animal.enclosure_type )
            and should_exclude_indoor_viewing_spot(
                  animal,
                  outdoor_likelihood=outdoor_likelihood_by_species_exhibit.get(
                     species_exhibit_key( animal ),
                     0 ) ) ):
         continue

      visible_animals.append( animal )

   return visible_animals
