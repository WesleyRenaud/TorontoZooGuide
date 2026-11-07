from __future__ import annotations

from pathlib import Path


class Paths():
   ROOT = Path( __file__ ).resolve().parents[ 2 ]
   DATABASE = ROOT / 'animals.db'
   EXHIBIT_DATA = ROOT / 'api' / 'seed' / 'data' / 'exhibit.json'
   REGION_TOKENS = ROOT / 'styles' / 'tokens.css'
   EMAIL_TEMPLATES = ROOT / 'tools' / 'checks' / 'email'
