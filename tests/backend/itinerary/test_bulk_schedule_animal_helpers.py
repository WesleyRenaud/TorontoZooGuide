from __future__ import annotations

from api.walk_graph.enclosure_viewing_walk_node_lookup import EnclosureViewingWalkNodeLookup


PAVILION = 'African Rainforest Pavilion'


def test_walk_node_id_by_enclosure_name_resolves_named_and_unnamed_viewing_spots() -> None:
   walk_node_ids = EnclosureViewingWalkNodeLookup.walk_node_id_by_enclosure_name()

   assert walk_node_ids[
      ( 'Marabou Stork', PAVILION, 'Savanna Overlook' )
   ] == 'v-0263'

   assert walk_node_ids[
      ( 'Ostrich', 'Africa Savanna', None )
   ] == 'v-0426'
