from __future__ import annotations

from ..models import Animal
from .walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot


def resolve_viewing_walk_node_id(
      species: str,
      exhibit: str,
      x_coord: float | None,
      y_coord: float | None,
      enclosure_name: str | None = None ) -> str | None:
   return walk_node_id_for_viewing_spot(
      species,
      exhibit,
      enclosure_name,
      x_coord,
      y_coord )


def apply_viewing_walk_node_id_to_animal( animal: Animal ) -> None:
   animal.viewing_walk_node_id = resolve_viewing_walk_node_id(
      animal.species,
      animal.exhibit,
      animal.x_coord,
      animal.y_coord,
      animal.enclosure_name )
