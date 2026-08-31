from __future__ import annotations

from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.walk_graph_spur import WalkGraphSpur
from api.walk_graph.walk_graph_spur_builder import WalkGraphSpurBuilder


def _node( node_id: str, x_px: float, y_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': y_px / 100.0,
      'x_px': x_px,
      'y_px': y_px,
   }


def _bridged_spur_graph() -> WalkGraph:
   main_node_count = 61
   spur_node_count = 15
   nodes = [
      _node( f'm-{ index }', float( index ), 0.0 )
      for index in range( main_node_count )
   ]
   nodes.extend(
      _node( f's-{ index }', float( main_node_count + index ), 0.0 )
      for index in range( spur_node_count ) )
   edges: list[ dict[ str, object ] ] = []

   for index in range( main_node_count - 1 ):
      from_id = f'm-{ index }'
      to_id = f'm-{ index + 1 }'
      edges.append( { 'from': from_id, 'to': to_id, 'length_px': 10.0 } )
      edges.append( { 'from': to_id, 'to': from_id, 'length_px': 10.0 } )

   edges.append( {
      'from': 'm-60',
      'to': 's-0',
      'length_px': 10.0,
   } )
   edges.extend( {
      'from': f's-{ index }',
      'to': f's-{ index + 1 }',
      'length_px': 10.0,
   }
      for index in range( spur_node_count - 1 ) )
   edges.extend( {
      'from': f's-{ index + 1 }',
      'to': f's-{ index }',
      'length_px': 10.0,
   }
      for index in range( spur_node_count - 1 ) )

   return {
      'map_width_px': 100,
      'map_height_px': 100,
      'entrance_node_id': 'm-0',
      'nodes': nodes,
      'edges': edges,
   }


PENINSULA_SPUR = WalkGraphSpur(
   node_ids=frozenset( { f's-{ index }' for index in range( 15 ) } ),
   attachment_node_ids=frozenset( { 'm-60' } ), )
OTHER_SPUR = WalkGraphSpur(
   node_ids=frozenset( { 'x-1', 'x-2' } ),
   attachment_node_ids=frozenset( { 'm-1' } ), )


def Test_IndexForViewingNodeIds_TestOverlappingSpur_ExpectBestMatch() -> None:
   spurs = [ OTHER_SPUR, PENINSULA_SPUR ]
   viewing_node_ids = [ 's-0', 's-5', 'x-1' ]

   assert WalkGraphSpurBuilder.index_for_viewing_node_ids(
      spurs,
      viewing_node_ids ) == 1


def Test_IndexForViewingNodeIds_TestNoOverlap_ExpectNone() -> None:
   assert WalkGraphSpurBuilder.index_for_viewing_node_ids(
      [ OTHER_SPUR ],
      [ 's-0' ] ) is None


def Test_IsActive_TestCurrentNodeInsideSpur_ExpectTrue() -> None:
   assert WalkGraphSpurBuilder.is_active(
      PENINSULA_SPUR,
      's-3',
      {} )


def Test_IsActive_TestNearAttachment_ExpectTrue() -> None:
   assert WalkGraphSpurBuilder.is_active(
      PENINSULA_SPUR,
      'outside-node',
      { 'm-60': 50.0 } )


def Test_IsActive_TestFarFromAttachment_ExpectFalse() -> None:
   assert not WalkGraphSpurBuilder.is_active(
      PENINSULA_SPUR,
      'outside-node',
      { 'm-60': 150.0 } )


def Test_BuildForGraph_TestBridgedPeninsula_ExpectSpurWithAttachmentNode() -> None:
   graph = _bridged_spur_graph()
   spurs = WalkGraphSpurBuilder.build_for_graph( graph )
   spur_index = WalkGraphSpurBuilder.index_for_viewing_node_ids(
      spurs,
      [ 's-0', 's-7', 's-14' ] )

   assert spur_index is not None

   spur = spurs[ spur_index ]

   assert len( spur.node_ids ) >= 15
   assert 's-0' in spur.node_ids
   assert 'm-60' in spur.attachment_node_ids
