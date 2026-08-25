from __future__ import annotations

from collections import defaultdict

from ...app_strings import format_app_string
from ...models import Animal
from ..search.animals_matching_query import species_exhibit_key
from ..search.species_exhibit_key import SpeciesExhibitKey
from ...shared.enums import EnclosureType


def complementary_indoor_likelihood( outdoor_likelihood: int ) -> int:
   return 100 - outdoor_likelihood


def single_habitat_alternate_enclosure_viewing_alert_message(
      animal: Animal ) -> str | None:
   enclosure_type = EnclosureType.normalize( animal.enclosure_type )
   if enclosure_type is None:
      return None

   return format_app_string(
      'guestStatus.animals.singleHabitatAlternateEnclosureViewingAlert',
      species=animal.species,
      chosenLocation=enclosure_type.viewing_location_label,
      alternateHabitat=EnclosureType.opposite_type( enclosure_type ).habitat_label )


def apply_single_habitat_alternate_enclosure_viewing_alert(
      animal: Animal,
      *,
      outdoor_likelihood: int ) -> None:
   effective_likelihood = effective_viewing_likelihood(
      animal,
      outdoor_likelihood=outdoor_likelihood,
      single_habitat=True )
   if effective_likelihood >= 100:
      return

   message = single_habitat_alternate_enclosure_viewing_alert_message( animal )
   if message is None:
      return

   animal.viewing_alert_messages.append( message )


def effective_viewing_likelihood(
      animal: Animal,
      *,
      outdoor_likelihood: int,
      single_habitat: bool ) -> int:
   if single_habitat and EnclosureType.is_indoor( animal.enclosure_type ):
      return complementary_indoor_likelihood( outdoor_likelihood )

   return animal.likelihood or 0


def single_habitat_viewing_species_exhibit_keys(
      animals: list[ Animal ] ) -> set[ SpeciesExhibitKey ]:
   candidate_keys = {
      species_exhibit_key( animal )
      for animal in animals
      if animal.include_all_viewing_spots is False
   }
   max_likelihood_by_key: dict[ SpeciesExhibitKey, int ] = defaultdict( int )

   for animal in animals:
      key = species_exhibit_key( animal )
      if key in candidate_keys:
         max_likelihood_by_key[ key ] = max(
            max_likelihood_by_key[ key ],
            animal.likelihood or 0 )

   return {
      key
      for key in candidate_keys
      if max_likelihood_by_key[ key ] > 0
   }


def preferred_viewing_spot_among(
      viewing_spots: list[ Animal ],
      *,
      outdoor_likelihood: int ) -> Animal:
   return max(
      viewing_spots,
      key=lambda animal: (
         effective_viewing_likelihood(
            animal,
            outdoor_likelihood=outdoor_likelihood,
            single_habitat=True ),
         EnclosureType.is_outdoor( animal.enclosure_type ),
      ) )


def preferred_single_habitat_viewing_spot_by_species_exhibit(
      animals: list[ Animal ],
      *,
      outdoor_likelihood_by_species_exhibit: dict[ SpeciesExhibitKey, int ],
      single_habitat_species_exhibit_keys: set[ SpeciesExhibitKey ] ) -> dict[ SpeciesExhibitKey, Animal ]:
   viewing_spots_by_species_exhibit: dict[ SpeciesExhibitKey, list[ Animal ] ] = defaultdict( list )

   for animal in animals:
      key = species_exhibit_key( animal )
      if key in single_habitat_species_exhibit_keys:
         viewing_spots_by_species_exhibit[ key ].append( animal )

   return {
      key: preferred_viewing_spot_among(
         viewing_spots,
         outdoor_likelihood=outdoor_likelihood_by_species_exhibit.get( key, 0 ) )
      for key, viewing_spots in viewing_spots_by_species_exhibit.items()
   }


def apply_indoor_outdoor_viewing_visibility(
      animals: list[ Animal ] ) -> list[ Animal ]:
   outdoor_likelihood_by_species_exhibit: dict[ SpeciesExhibitKey, int ] = {}
   single_habitat_species_exhibit_keys = single_habitat_viewing_species_exhibit_keys(
      animals )

   for animal in animals:
      if not EnclosureType.is_outdoor( animal.enclosure_type ):
         continue

      key = species_exhibit_key( animal )
      outdoor_likelihood_by_species_exhibit[ key ] = max(
         outdoor_likelihood_by_species_exhibit.get( key, 0 ),
         animal.likelihood or 0 )

   preferred_viewing_spot_by_species_exhibit = (
      preferred_single_habitat_viewing_spot_by_species_exhibit(
         animals,
         outdoor_likelihood_by_species_exhibit=outdoor_likelihood_by_species_exhibit,
         single_habitat_species_exhibit_keys=single_habitat_species_exhibit_keys ) )

   visible_animals: list[ Animal ] = []

   for animal in animals:
      key = species_exhibit_key( animal )
      outdoor_likelihood = outdoor_likelihood_by_species_exhibit.get( key, 0 )
      is_single_habitat = key in single_habitat_species_exhibit_keys

      if (
            is_single_habitat
            and preferred_viewing_spot_by_species_exhibit.get( key ) is not animal ):
         continue

      if is_single_habitat:
         apply_single_habitat_alternate_enclosure_viewing_alert(
            animal,
            outdoor_likelihood=outdoor_likelihood )

      if is_single_habitat and EnclosureType.is_indoor( animal.enclosure_type ):
         animal.likelihood = 100

      visible_animals.append( animal )

   return visible_animals
