from __future__ import annotations

import re

from .color_token import ColorToken
from .paths import Paths


class ColorTokens():
   TOKEN_RE = re.compile(
      r'--(?P<name>color-[a-z0-9-]+):\s*(?P<color>#[0-9A-Fa-f]{6})\s*;'
   )
   _colors: dict[ str, str ] = {
      match.group( 'name' ): match.group( 'color' )
      for match in TOKEN_RE.finditer( Paths.REGION_TOKENS.read_text() )
   }


   @classmethod
   def color( cls, token: ColorToken ) -> str:
      return cls._colors[ token.value ]
