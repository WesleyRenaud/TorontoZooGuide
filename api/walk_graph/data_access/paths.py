from __future__ import annotations

from pathlib import Path


API_ROOT = Path( __file__ ).resolve().parents[ 2 ]
SEED_DATA_DIR = API_ROOT / 'seed' / 'data'
WALK_GRAPH_PATH = SEED_DATA_DIR / 'walk_graph.json'
ENCLOSURE_VIEWING_WALK_NODE_PATH = SEED_DATA_DIR / 'enclosure_viewing_walk_node.json'
ATTRACTION_WALK_NODE_PATH = SEED_DATA_DIR / 'attraction_walk_node.json'
GUARDIANS_TALK_WALK_NODE_PATH = SEED_DATA_DIR / 'guardians_talk_walk_node.json'
WILD_ENCOUNTER_MEETING_SPOT_WALK_NODE_PATH = (
   SEED_DATA_DIR / 'wild_encounter_meeting_spot_walk_node.json' )
MAP_LOCATION_WALK_NODE_PATHS = (
   ATTRACTION_WALK_NODE_PATH,
   GUARDIANS_TALK_WALK_NODE_PATH,
   WILD_ENCOUNTER_MEETING_SPOT_WALK_NODE_PATH,
)
MAX_ENCLOSURE_VIEWING_SNAP_DISTANCE_PX = 220.0
MAX_MAP_LOCATION_SNAP_DISTANCE_PX = 400.0
