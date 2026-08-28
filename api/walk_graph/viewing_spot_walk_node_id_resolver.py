from __future__ import annotations

from .enclosure_viewing_walk_node_lookup import walk_node_for_viewing_spot
from .enclosure_viewing_walk_node_lookup import walk_node_id_by_enclosure_name


class ViewingSpotWalkNodeIdResolver():
   @classmethod
   def resolve(
         cls,
         species: str,
         exhibit: str,
         enclosure_name: str | None,
         x_coord: float | None = None,
         y_coord: float | None = None ) -> str | None:
      walk_node_id = walk_node_id_by_enclosure_name().get(
         ( species, exhibit, enclosure_name ) )

      if walk_node_id is not None:
         return walk_node_id

      return cls.resolve_for_coordinates(
         species,
         exhibit,
         x_coord,
         y_coord )


   @classmethod
   def resolve_for_coordinates(
         cls,
         species: str,
         exhibit: str,
         x_coord: float | None,
         y_coord: float | None ) -> str | None:
      if x_coord is None or y_coord is None:
         return None

      viewing_spot = walk_node_for_viewing_spot(
         species,
         exhibit,
         x_coord,
         y_coord )

      if viewing_spot is None:
         return None

      return str( viewing_spot[ 'walk_node_id' ] )
