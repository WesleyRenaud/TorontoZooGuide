from __future__ import annotations

import json
from pathlib import Path


class Paths():
   ROOT = Path( __file__ ).resolve().parents[ 2 ]
   DETAIL_IMAGES = ROOT / json.loads(
      ( ROOT / 'shared' / 'detailImages.json' ).read_text()
   )[ 'root' ]
   DATABASE = ROOT / 'animals.db'
   EXHIBIT_DATA = ROOT / 'api' / 'seed' / 'data' / 'exhibit.json'
   ATTRACTION_DATA = ROOT / 'api' / 'seed' / 'data' / 'attraction.json'
   RESTAURANT_DATA = ROOT / 'api' / 'seed' / 'data' / 'restaurant.json'
   GIFT_SHOP_DATA = ROOT / 'api' / 'seed' / 'data' / 'gift_shop.json'
   REGION_TOKENS = ROOT / 'styles' / 'tokens.css'
   EMAIL_TEMPLATES = ROOT / 'tools' / 'checks' / 'email'
