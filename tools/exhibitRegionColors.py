from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path( __file__ ).resolve().parents[ 1 ]
EXHIBIT_PATH = ROOT / 'api' / 'seed' / 'data' / 'exhibit.json'
TOKENS_PATH = ROOT / 'styles' / 'tokens.css'
TOKEN_RE = re.compile(
   r'--color-region-(?P<slug>[a-z0-9-]+)-(?P<part>bg|text):\s*(?P<color>#[0-9A-Fa-f]{6})'
)


def exhibit_region( exhibit: str ) -> str | None:
   folded = exhibit.casefold()

   for row in json.loads( EXHIBIT_PATH.read_text() ):
      if row[ 'name' ].casefold() == folded:
         return row[ 'region' ]

   return None


def region_slug( region: str ) -> str:
   return region.casefold().replace( ' ', '-' )


def region_colors( region: str ) -> tuple[ str, str ]:
   slug = region_slug( region )
   parts: dict[ str, str ] = {}

   for match in TOKEN_RE.finditer( TOKENS_PATH.read_text() ):
      if match.group( 'slug' ) != slug:
         continue

      parts[ match.group( 'part' ) ] = match.group( 'color' )

   if 'bg' not in parts or 'text' not in parts:
      raise RuntimeError( f'The region colors do not include { region }.' )

   return ( parts[ 'bg' ], parts[ 'text' ] )


def exhibit_colors( exhibit: str ) -> tuple[ str, str ] | None:
   region = exhibit_region( exhibit )

   if region == None:
      return None

   return region_colors( region )
