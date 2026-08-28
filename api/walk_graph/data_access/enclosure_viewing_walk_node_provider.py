from __future__ import annotations

import json
from pathlib import Path

from ..domain.enclosure_viewing_walk_node import EnclosureViewingWalkNode
from .paths import Paths


class EnclosureViewingWalkNodeProvider():
   @classmethod
   def fetch_records(
         cls,
         path: Path = Paths.ENCLOSURE_VIEWING_WALK_NODE_PATH ) -> list[ EnclosureViewingWalkNode ]:
      return json.loads( path.read_text( encoding='utf-8' ) )
