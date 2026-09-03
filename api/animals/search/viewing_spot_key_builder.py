from __future__ import annotations

from typing import Any

from ...models.animal import Animal
from ...shared.value_conversion import ValueConversion
from .species_exhibit_key_builder import SpeciesExhibitKeyBuilder


class ViewingSpotKeyBuilder():
   @classmethod
   def name_from_value( cls, value: Any ) -> str | None:
      return ValueConversion.as_nullable_string( value )


   @classmethod
   def from_values(
         cls,
         species: str,
         exhibit: str,
         enclosure_name: Any = None ) -> tuple[ str, str, str | None ]:
      key = SpeciesExhibitKeyBuilder.from_values( species, exhibit )

      return (
         key.species,
         key.exhibit,
         cls.name_from_value( enclosure_name ),
      )


   @classmethod
   def from_animal( cls, animal: Animal ) -> tuple[ str, str, str | None ]:
      return cls.from_values(
         animal.species,
         animal.exhibit,
         animal.enclosure_name )
