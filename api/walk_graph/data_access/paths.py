from __future__ import annotations

from pathlib import Path


API_ROOT = Path( __file__ ).resolve().parents[ 2 ]
SEED_DATA_DIR = API_ROOT / 'seed' / 'data'
WALK_GRAPH_PATH = SEED_DATA_DIR / 'walk_graph.json'
ENCLOSURE_VIEWING_WALK_NODE_PATH = SEED_DATA_DIR / 'enclosure_viewing_walk_node.json'
MAX_ENCLOSURE_VIEWING_SNAP_DISTANCE_PX = 220.0
