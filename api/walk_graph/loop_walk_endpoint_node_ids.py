from __future__ import annotations

from .domain.master_route_loop import MasterRouteLoop
from .domain.viewing_spot_reference import ViewingSpotReference
from .walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot


def loop_walk_endpoint_node_ids(
      loop: MasterRouteLoop ) -> tuple[ str | None, str | None ]:
   if not loop.viewing_spots:
      return None, None

   first_viewing_spot = loop.viewing_spots[ 0 ]
   last_viewing_spot = loop.viewing_spots[ -1 ]

   return (
      _walk_node_id_for_viewing_spot_reference( first_viewing_spot ),
      _walk_node_id_for_viewing_spot_reference( last_viewing_spot ),
   )


def _walk_node_id_for_viewing_spot_reference(
      viewing_spot: ViewingSpotReference ) -> str | None:
   return walk_node_id_for_viewing_spot(
      viewing_spot.species,
      viewing_spot.exhibit,
      viewing_spot.name )
