from __future__ import annotations

import json
from pathlib import Path

from ..domain.enclosure_viewing_walk_node import EnclosureViewingWalkNode
from .paths import ENCLOSURE_VIEWING_WALK_NODE_PATH


def load_enclosure_viewing_walk_nodes(
      path: Path = ENCLOSURE_VIEWING_WALK_NODE_PATH ) -> list[ EnclosureViewingWalkNode ]:
   return json.loads( path.read_text( encoding='utf-8' ) )
