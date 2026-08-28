from __future__ import annotations

from .viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


class ViewingWalkNodeIdResolver():
   @classmethod
   def resolve(
         cls,
         species: str,
         exhibit: str,
         x_coord: float | None,
         y_coord: float | None,
         enclosure_name: str | None = None ) -> str | None:
      return ViewingSpotWalkNodeIdResolver.resolve(
         species,
         exhibit,
         enclosure_name,
         x_coord,
         y_coord )
