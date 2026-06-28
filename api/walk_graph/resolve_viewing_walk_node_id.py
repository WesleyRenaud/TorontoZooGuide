from __future__ import annotations

from .enclosure_viewing_walk_node_lookup import walk_node_for_viewing_spot
from ..models import Animal


def resolve_viewing_walk_node_id(
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


def apply_viewing_walk_node_id_to_animal( animal: Animal ) -> None:
   animal.viewing_walk_node_id = resolve_viewing_walk_node_id(
      animal.species,
      animal.exhibit,
      animal.x_coord,
      animal.y_coord )
