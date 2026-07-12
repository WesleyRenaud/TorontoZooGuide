from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
import json

from ..animals.search.species_exhibit_key import SpeciesExhibitKey
from .data_access.load_enclosure_viewing_walk_nodes import load_enclosure_viewing_walk_nodes
from .data_access.paths import ENCLOSURE_VIEWING_PATH
from .domain.enclosure_viewing_walk_node import EnclosureViewingWalkNode
from .domain.viewing_spot_key import viewing_spot_key
from .domain.viewing_spot_key import viewing_spot_key_from_enclosure_viewing_row
from .domain.viewing_spot_key import viewing_spot_key_from_walk_node_row
from .domain.viewing_spot_key import ViewingSpotKey
from ..shared.value_conversion import ValueConversion


EnclosureNameViewingSpotKey = tuple[ str, str, str | None ]


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
def walk_node_id_by_enclosure_name() -> dict[ EnclosureNameViewingSpotKey, str ]:
   walk_nodes_by_spot = enclosure_viewing_walk_nodes_by_viewing_spot()
   walk_node_ids: dict[ EnclosureNameViewingSpotKey, str ] = {}

   for row in json.loads( ENCLOSURE_VIEWING_PATH.read_text( encoding='utf-8' ) ):
      walk_node = walk_nodes_by_spot.get(
         viewing_spot_key_from_enclosure_viewing_row( row ) )

      if walk_node == None:
         continue

      walk_node_ids[
         (
            str( row[ 'species' ] ),
            str( row[ 'exhibit' ] ),
            ValueConversion.as_nullable_string( row.get( 'name' ) ),
         )
      ] = str( walk_node[ 'walk_node_id' ] )

   return walk_node_ids


@lru_cache( maxsize=1 )
def walk_nodes_grouped_by_species_exhibit() -> dict[
      SpeciesExhibitKey,
      list[ EnclosureViewingWalkNode ],
   ]:
   grouped: dict[ SpeciesExhibitKey, list[ EnclosureViewingWalkNode ] ] = defaultdict( list )

   for row in load_enclosure_viewing_walk_nodes():
      grouped[
         SpeciesExhibitKey.from_values( row[ 'species' ], row[ 'exhibit' ] )
      ].append( row )

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
      walk_nodes_grouped_by_species_exhibit().get(
         SpeciesExhibitKey.from_values( species, exhibit ),
         [] ) )
