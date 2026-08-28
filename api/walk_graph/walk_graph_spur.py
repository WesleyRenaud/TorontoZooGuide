from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class WalkGraphSpur:
   node_ids: frozenset[ str ]
   attachment_node_ids: frozenset[ str ]
