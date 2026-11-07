from __future__ import annotations

from functools import cache
import re

from .font_family import FontFamily
from .paths import Paths


class FontTokens():
   TOKEN_RE = re.compile(
      r"--(?P<name>font-family-[a-z0-9-]+):\s*(?P<font>[^;]+?)\s*;"
   )


   @classmethod
   @cache
   def _load_fonts( cls ) -> list[ FontFamily ]:
      return [
         FontFamily( name=match.group( 'name' ), font=match.group( 'font' ) )
         for match in cls.TOKEN_RE.finditer( Paths.REGION_TOKENS.read_text() )
      ]


   @classmethod
   def font( cls, name: str ) -> str:
      return next( item.font for item in cls._load_fonts() if item.name == name )
