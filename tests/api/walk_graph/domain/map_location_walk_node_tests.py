from __future__ import annotations

from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.domain.map_location_walk_node import MapLocationWalkNode


def Test_ToJson_TestNamedEnclosure_ExpectEnclosureIncluded() -> None:
   enclosure_name = 'Giraffe House'
   node = MapLocationWalkNode(
      kind=MapLocationKind.GUARDIANS_TALK,
      name='Masai Giraffe',
      location='Africa Savanna',
      x=1.0,
      y=2.0,
      walk_node_id='v-0298',
      snap_distance_px=3.0,
      enclosure_name=enclosure_name )

   row = node.to_json()

   assert row[ 'enclosure_name' ] == node.enclosure_name
