from __future__ import annotations

from dataclasses import dataclass

from .map_location_key import MapLocationKey
from .map_location_kind import MapLocationKind


@dataclass( frozen=True )
class MapLocationWalkNode:
   kind: MapLocationKind
   name: str
   location: str
   x: float
   y: float
   walk_node_id: str
   snap_distance_px: float


   def location_key( self ) -> MapLocationKey:
      return MapLocationKey(
         kind=self.kind,
         name=self.name,
         location=self.location )


   def sort_key( self ) -> tuple[ str, str, str ]:
      return self.location_key().sort_key()


   @classmethod
   def from_json( cls, row: dict[ str, object ] ) -> MapLocationWalkNode:
      return cls(
         kind=MapLocationKind( str( row[ 'kind' ] ) ),
         name=str( row[ 'name' ] ),
         location=str( row[ 'location' ] ),
         x=float( row[ 'x' ] ),
         y=float( row[ 'y' ] ),
         walk_node_id=str( row[ 'walk_node_id' ] ),
         snap_distance_px=float( row[ 'snap_distance_px' ] ) )


   def to_json( self ) -> dict[ str, object ]:
      return {
         'kind': self.kind.value,
         'name': self.name,
         'location': self.location,
         'x': self.x,
         'y': self.y,
         'walk_node_id': self.walk_node_id,
         'snap_distance_px': self.snap_distance_px,
      }
