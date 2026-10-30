from __future__ import annotations

from dataclasses import dataclass

from .map_location_kind import MapLocationKind


@dataclass( frozen=True )
class MapLocationKey:
   kind: MapLocationKind
   name: str
   location: str = ''
   enclosure_name: str = ''


   @staticmethod
   def for_kind(
         kind: MapLocationKind,
         name: str,
         *,
         location: str = '',
         enclosure_name: str | None = '' ) -> MapLocationKey:
      return MapLocationKey(
         kind=kind,
         name=name,
         location=location,
         enclosure_name=enclosure_name or '' )


   def sort_key( self ) -> tuple[ str, str, str, str ]:
      return (
         self.kind.value,
         self.name.lower(),
         self.location.lower(),
         self.enclosure_name.lower(),
      )
