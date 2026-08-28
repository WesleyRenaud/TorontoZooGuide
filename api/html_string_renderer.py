from __future__ import annotations

import html
import re

from .app_string_provider import AppStringProvider


HTML_STRING_TOKEN_RE = re.compile( r'\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}' )


class HtmlStringRenderer():
   @classmethod
   def clear_cache( cls ) -> None:
      AppStringProvider.clear_cache()


   @classmethod
   def values( cls ) -> dict[ str, str ]:
      return AppStringProvider.values()


   @classmethod
   def render(
         cls,
         content: str ) -> str:
      string_values = cls.values()

      def replace_token( match: re.Match[ str ] ) -> str:
         key = match.group( 1 )
         value = string_values.get( key )

         if value is None:
            return match.group( 0 )

         return html.escape( value, quote=True )

      return HTML_STRING_TOKEN_RE.sub( replace_token, content )
