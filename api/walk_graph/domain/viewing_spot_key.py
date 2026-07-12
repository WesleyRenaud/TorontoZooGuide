from __future__ import annotations

from .enclosure_viewing_walk_node import EnclosureViewingWalkNode


ViewingSpotKey = tuple[ str, str, float, float ]


def viewing_spot_key(
      species: str,
      exhibit: str,
      x: float,
      y: float ) -> ViewingSpotKey:
   return ( species, exhibit, x, y )


def viewing_spot_key_from_walk_node_row(
      row: EnclosureViewingWalkNode ) -> ViewingSpotKey:
   return viewing_spot_key(
      row[ 'species' ],
      row[ 'exhibit' ],
      row[ 'x' ],
      row[ 'y' ] )


def viewing_spot_key_from_enclosure_viewing_row(
      row: dict[ str, object ] ) -> ViewingSpotKey:
   return viewing_spot_key(
      str( row[ 'species' ] ),
      str( row[ 'exhibit' ] ),
      float( row[ 'x_coord' ] ),
      float( row[ 'y_coord' ] ) )
