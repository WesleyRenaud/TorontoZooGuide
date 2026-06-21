from __future__ import annotations

import json
from pathlib import Path

from ..domain.walk_graph import WalkGraph
from .paths import WALK_GRAPH_PATH


def load_walk_graph( path: Path = WALK_GRAPH_PATH ) -> WalkGraph:
   return json.loads( path.read_text( encoding='utf-8' ) )
