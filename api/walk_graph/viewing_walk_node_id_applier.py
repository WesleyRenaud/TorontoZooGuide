from __future__ import annotations

from ..models import Animal
from .viewing_walk_node_id_resolver import ViewingWalkNodeIdResolver


class ViewingWalkNodeIdApplier():
   @classmethod
   def apply( cls, animal: Animal ) -> None:
      animal.viewing_walk_node_id = ViewingWalkNodeIdResolver.resolve(
         animal.species,
         animal.exhibit,
         animal.x_coord,
         animal.y_coord,
         animal.enclosure_name )
