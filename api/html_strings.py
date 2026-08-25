from __future__ import annotations

import html
import re

from .app_strings import clear_app_string_cache
from .app_strings import get_app_string_values


HTML_STRING_TOKEN_RE = re.compile( r'\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}' )


def clear_html_string_cache() -> None:
   clear_app_string_cache()


def get_html_string_values() -> dict[ str, str ]:
   return get_app_string_values()


def render_html_strings( content: str ) -> str:
   string_values = get_html_string_values()

   def replace_token( match: re.Match[ str ] ) -> str:
      key = match.group( 1 )
      value = string_values.get( key )

      if value is None:
         return match.group( 0 )

      return html.escape( value, quote=True )

   return HTML_STRING_TOKEN_RE.sub( replace_token, content )
