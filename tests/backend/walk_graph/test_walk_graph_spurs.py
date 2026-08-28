from __future__ import annotations

from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.enclosure_viewing_walk_node_lookup import EnclosureViewingWalkNodeLookup
from api.walk_graph.walk_graph_spur_builder import WalkGraphSpurBuilder


def test_walk_graph_spurs_detects_canadian_domain_peninsula() -> None:
   graph = WalkGraphProvider.fetch()
   spurs = WalkGraphSpurBuilder.build_for_graph( graph )
   canada_node_ids = tuple( {
      walk_node_id
      for ( _species, exhibit, _enclosure_name ), walk_node_id
         in EnclosureViewingWalkNodeLookup.walk_node_id_by_enclosure_name().items()
      if exhibit == 'Canadian Domain'
   } )

   canada_spur_index = WalkGraphSpurBuilder.index_for_viewing_node_ids(
      spurs,
      canada_node_ids )

   assert canada_spur_index is not None

   canada_spur = spurs[ canada_spur_index ]

   assert len( canada_spur.node_ids ) >= 15
   assert canada_node_ids[ 0 ] in canada_spur.node_ids
   assert canada_spur.attachment_node_ids

   watusi_node_id = EnclosureViewingWalkNodeLookup.walk_node_id_by_enclosure_name()[
      ( 'Watusi Cattle', 'Africa Savanna', None ) ]

   assert (
      watusi_node_id in canada_spur.attachment_node_ids
      or watusi_node_id in canada_spur.node_ids
   )
