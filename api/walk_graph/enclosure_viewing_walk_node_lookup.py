from __future__ import annotations

from collections import defaultdict
from functools import lru_cache

from .data_access.load_enclosure_viewing_walk_nodes import load_enclosure_viewing_walk_nodes
from .domain.enclosure_viewing_walk_node import EnclosureViewingWalkNode
from .domain.viewing_spot_key import SpeciesExhibitKey
from .domain.viewing_spot_key import viewing_spot_key
from .domain.viewing_spot_key import viewing_spot_key_from_walk_node_row
from .domain.viewing_spot_key import ViewingSpotKey


@lru_cache( maxsize=1 )
def enclosure_viewing_walk_nodes_by_viewing_spot() -> dict[
      ViewingSpotKey,
      EnclosureViewingWalkNode,
   ]:
   return {
      viewing_spot_key_from_walk_node_row( row ): row
      for row in load_enclosure_viewing_walk_nodes()
   }


@lru_cache( maxsize=1 )
def walk_nodes_grouped_by_species_exhibit() -> dict[
      SpeciesExhibitKey,
      list[ EnclosureViewingWalkNode ],
   ]:
   grouped: dict[ SpeciesExhibitKey, list[ EnclosureViewingWalkNode ] ] = defaultdict( list )

   for row in load_enclosure_viewing_walk_nodes():
      grouped[ ( row[ 'species' ], row[ 'exhibit' ] ) ].append( row )

   return dict( grouped )


def walk_node_for_viewing_spot(
      species: str,
      exhibit: str,
      x: float,
      y: float ) -> EnclosureViewingWalkNode | None:
   return enclosure_viewing_walk_nodes_by_viewing_spot().get(
      viewing_spot_key( species, exhibit, x, y ) )


def walk_nodes_for_species_exhibit(
      species: str,
      exhibit: str ) -> list[ EnclosureViewingWalkNode ]:
   return list(
      walk_nodes_grouped_by_species_exhibit().get( ( species, exhibit ), [] ) )
