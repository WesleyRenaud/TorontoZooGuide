from __future__ import annotations

from .enclosure_viewing_walk_node import EnclosureViewingWalkNode
from .viewing_spot_key import ViewingSpotKey


class ViewingSpotKeyBuilder():
   @classmethod
   def from_coordinates(
         cls,
         species: str,
         exhibit: str,
         x: float,
         y: float ) -> ViewingSpotKey:
      return ( species, exhibit, x, y )


   @classmethod
   def from_walk_node_row(
         cls,
         row: EnclosureViewingWalkNode ) -> ViewingSpotKey:
      return cls.from_coordinates(
         row[ 'species' ],
         row[ 'exhibit' ],
         row[ 'x' ],
         row[ 'y' ] )


   @classmethod
   def from_enclosure_viewing_row(
         cls,
         row: dict[ str, object ] ) -> ViewingSpotKey:
      return cls.from_coordinates(
         str( row[ 'species' ] ),
         str( row[ 'exhibit' ] ),
         float( row[ 'x_coord' ] ),
         float( row[ 'y_coord' ] ) )
