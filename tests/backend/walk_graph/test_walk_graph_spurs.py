from __future__ import annotations

from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.enclosure_viewing_walk_node_lookup import walk_node_id_by_enclosure_name
from api.walk_graph.walk_graph_spurs import walk_graph_spur_index_for_viewing_node_ids
from api.walk_graph.walk_graph_spurs import walk_graph_spurs_for_graph


def test_walk_graph_spurs_detects_canadian_domain_peninsula() -> None:
   graph = load_walk_graph()
   spurs = walk_graph_spurs_for_graph( graph )
   canada_node_ids = tuple( {
      walk_node_id
      for ( _species, exhibit, _enclosure_name ), walk_node_id
         in walk_node_id_by_enclosure_name().items()
      if exhibit == 'Canadian Domain'
   } )

   canada_spur_index = walk_graph_spur_index_for_viewing_node_ids(
      spurs,
      canada_node_ids )

   assert canada_spur_index is not None

   canada_spur = spurs[ canada_spur_index ]

   assert len( canada_spur.node_ids ) >= 15
   assert canada_node_ids[ 0 ] in canada_spur.node_ids
   assert canada_spur.attachment_node_ids

   watusi_node_id = walk_node_id_by_enclosure_name()[
      ( 'Watusi Cattle', 'Africa Savanna', None ) ]

   assert (
      watusi_node_id in canada_spur.attachment_node_ids
      or watusi_node_id in canada_spur.node_ids
   )
