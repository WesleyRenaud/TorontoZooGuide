from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .viewing_spot_reference import viewing_spot_reference_from_json
from .viewing_spot_reference import ViewingSpotReference


@dataclass( frozen=True )
class ViewingSpotRoutingOverride:
   override_id: str
   viewing_spot: ViewingSpotReference
   scheduling_walk_node_id: str
   visit_before: tuple[ ViewingSpotReference, ... ]


def viewing_spot_routing_override_from_json(
      path: Path ) -> ViewingSpotRoutingOverride:
   payload = json.loads( path.read_text( encoding='utf-8' ) )

   return ViewingSpotRoutingOverride(
      override_id=str( payload[ 'id' ] ),
      viewing_spot=viewing_spot_reference_from_json(
         payload[ 'viewing_spot' ] ),
      scheduling_walk_node_id=str( payload[ 'scheduling_walk_node_id' ] ),
      visit_before=tuple(
         viewing_spot_reference_from_json( row )
         for row in payload.get( 'visit_before', [] ) ) )
