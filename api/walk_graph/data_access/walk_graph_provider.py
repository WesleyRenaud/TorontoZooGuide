from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path

from ..domain.walk_graph import WalkGraph
from .paths import WALK_GRAPH_PATH


class WalkGraphProvider():
   @classmethod
   @lru_cache( maxsize=1 )
   def fetch( cls, path: Path = WALK_GRAPH_PATH ) -> WalkGraph:
      return json.loads( path.read_text( encoding='utf-8' ) )
