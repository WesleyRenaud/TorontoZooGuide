from __future__ import annotations

from dataclasses import dataclass

from ...shared.value_conversion import ValueConversion
from .viewing_spot_name_key import ViewingSpotNameKey


@dataclass( frozen=True )
class ViewingSpotReference:
   species: str
   exhibit: str
   name: str | None

   def key( self ) -> ViewingSpotNameKey:
      return ( self.species, self.exhibit, self.name )


def viewing_spot_reference_from_json(
      payload: dict[ str, object ] ) -> ViewingSpotReference:
   return ViewingSpotReference(
      species=str( payload[ 'species' ] ),
      exhibit=str( payload[ 'exhibit' ] ),
      name=ValueConversion.as_nullable_string( payload.get( 'name' ) ) )
