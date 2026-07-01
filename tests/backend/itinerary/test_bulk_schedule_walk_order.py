from __future__ import annotations

from api.itinerary.scheduling.bulk.bulk_schedule_walk_order import representative_walk_node_id
from api.itinerary.scheduling.bulk.bulk_schedule_walk_order import walk_travel_distance_px
from api.walk_graph.data_access.load_walk_graph import load_walk_graph


def test_representative_walk_node_id_prefers_closest_viewing_spot() -> None:
   graph = load_walk_graph()
   entrance_node_id = str( graph[ 'entrance_node_id' ] )

   assert representative_walk_node_id(
      graph,
      entrance_node_id,
      'Cheetah',
      'Indo-Malaya Outdoor' ) == 'v-0226'
