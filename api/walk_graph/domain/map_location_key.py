from __future__ import annotations

from dataclasses import dataclass

from .map_location_kind import MapLocationKind


@dataclass( frozen=True )
class MapLocationKey:
   kind: MapLocationKind
   name: str
   location: str = ''


   @staticmethod
   def for_kind(
         kind: MapLocationKind,
         name: str,
         *,
         location: str = '' ) -> MapLocationKey:
      return MapLocationKey( kind=kind, name=name, location=location )


   def sort_key( self ) -> tuple[ str, str, str ]:
      return ( self.kind.value, self.name.lower(), self.location.lower() )
