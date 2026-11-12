from __future__ import annotations

import re


class PatternGroup():
   @classmethod
   def first(
         cls,
         text: str,
         name: str,
         *patterns: re.Pattern[ str ] ) -> str | None:
      for pattern in patterns:
         match = pattern.search( text )

         if match != None:
            return match.group( name )

      return None
