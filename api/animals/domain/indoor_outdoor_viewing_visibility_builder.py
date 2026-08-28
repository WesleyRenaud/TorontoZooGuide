from __future__ import annotations

from collections import defaultdict

from ...app_strings import AppStringProvider
from ...models import Animal
from ..search.species_exhibit_key import SpeciesExhibitKey
from ..search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from ...shared.enums import EnclosureType


class IndoorOutdoorViewingVisibilityBuilder():
   @classmethod
   def _complementary_indoor_likelihood( cls, outdoor_likelihood: int ) -> int:
      return 100 - outdoor_likelihood


   @classmethod
   def single_habitat_alternate_enclosure_viewing_alert_message(
         cls,
         animal: Animal ) -> str | None:
      enclosure_type = EnclosureType.normalize( animal.enclosure_type )
      if enclosure_type is None:
         return None

      return AppStringProvider.format(
         'guestStatus.animals.singleHabitatAlternateEnclosureViewingAlert',
         species=animal.species,
         chosenLocation=enclosure_type.viewing_location_label,
         alternateHabitat=EnclosureType.opposite_type( enclosure_type ).habitat_label )


   @classmethod
   def apply_single_habitat_alternate_enclosure_viewing_alert(
         cls,
         animal: Animal,
         *,
         outdoor_likelihood: int ) -> None:
      effective_likelihood = cls.effective_viewing_likelihood(
         animal,
         outdoor_likelihood=outdoor_likelihood,
         single_habitat=True )
      if effective_likelihood >= 100:
         return

      message = cls.single_habitat_alternate_enclosure_viewing_alert_message( animal )
      if message is None:
         return

      animal.viewing_alert_messages.append( message )


   @classmethod
   def effective_viewing_likelihood(
         cls,
         animal: Animal,
         *,
         outdoor_likelihood: int,
         single_habitat: bool ) -> int:
      if single_habitat and EnclosureType.is_indoor( animal.enclosure_type ):
         return cls._complementary_indoor_likelihood( outdoor_likelihood )

      return animal.likelihood or 0


   @classmethod
   def single_habitat_viewing_species_exhibit_keys(
         cls,
         animals: list[ Animal ] ) -> set[ SpeciesExhibitKey ]:
      candidate_keys = {
         SpeciesExhibitKeyBuilder.from_animal( animal )
         for animal in animals
         if animal.include_all_viewing_spots is False
      }
      max_likelihood_by_key: dict[ SpeciesExhibitKey, int ] = defaultdict( int )

      for animal in animals:
         key = SpeciesExhibitKeyBuilder.from_animal( animal )
         if key in candidate_keys:
            max_likelihood_by_key[ key ] = max(
               max_likelihood_by_key[ key ],
               animal.likelihood or 0 )

      return {
         key
         for key in candidate_keys
         if max_likelihood_by_key[ key ] > 0
      }


   @classmethod
   def _preferred_viewing_spot_among(
         cls,
         viewing_spots: list[ Animal ],
         *,
         outdoor_likelihood: int ) -> Animal:
      return max(
         viewing_spots,
         key=lambda animal: (
            cls.effective_viewing_likelihood(
               animal,
               outdoor_likelihood=outdoor_likelihood,
               single_habitat=True ),
            EnclosureType.is_outdoor( animal.enclosure_type ),
         ) )


   @classmethod
   def preferred_single_habitat_viewing_spot_by_species_exhibit(
         cls,
         animals: list[ Animal ],
         *,
         outdoor_likelihood_by_species_exhibit: dict[ SpeciesExhibitKey, int ],
         single_habitat_species_exhibit_keys: set[ SpeciesExhibitKey ] ) -> dict[ SpeciesExhibitKey, Animal ]:
      viewing_spots_by_species_exhibit: dict[ SpeciesExhibitKey, list[ Animal ] ] = defaultdict( list )

      for animal in animals:
         key = SpeciesExhibitKeyBuilder.from_animal( animal )
         if key in single_habitat_species_exhibit_keys:
            viewing_spots_by_species_exhibit[ key ].append( animal )

      return {
         key: cls._preferred_viewing_spot_among(
            viewing_spots,
            outdoor_likelihood=outdoor_likelihood_by_species_exhibit.get( key, 0 ) )
         for key, viewing_spots in viewing_spots_by_species_exhibit.items()
      }


   @classmethod
   def apply(
         cls,
         animals: list[ Animal ] ) -> list[ Animal ]:
      outdoor_likelihood_by_species_exhibit: dict[ SpeciesExhibitKey, int ] = {}
      single_habitat_species_exhibit_keys = cls.single_habitat_viewing_species_exhibit_keys(
         animals )

      for animal in animals:
         if not EnclosureType.is_outdoor( animal.enclosure_type ):
            continue

         key = SpeciesExhibitKeyBuilder.from_animal( animal )
         outdoor_likelihood_by_species_exhibit[ key ] = max(
            outdoor_likelihood_by_species_exhibit.get( key, 0 ),
            animal.likelihood or 0 )

      preferred_viewing_spot_by_species_exhibit = (
         cls.preferred_single_habitat_viewing_spot_by_species_exhibit(
            animals,
            outdoor_likelihood_by_species_exhibit=outdoor_likelihood_by_species_exhibit,
            single_habitat_species_exhibit_keys=single_habitat_species_exhibit_keys ) )

      visible_animals: list[ Animal ] = []

      for animal in animals:
         key = SpeciesExhibitKeyBuilder.from_animal( animal )
         outdoor_likelihood = outdoor_likelihood_by_species_exhibit.get( key, 0 )
         is_single_habitat = key in single_habitat_species_exhibit_keys

         if (
               is_single_habitat
               and preferred_viewing_spot_by_species_exhibit.get( key ) is not animal ):
            continue

         if is_single_habitat:
            cls.apply_single_habitat_alternate_enclosure_viewing_alert(
               animal,
               outdoor_likelihood=outdoor_likelihood )

         if is_single_habitat and EnclosureType.is_indoor( animal.enclosure_type ):
            animal.likelihood = 100

         visible_animals.append( animal )

      return visible_animals
