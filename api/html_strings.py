from __future__ import annotations

import html
import json
import re
import subprocess
from typing import Any


STRING_EXPORT_SCRIPT = './tools/exportStringValues.mjs'
HTML_STRING_TOKEN_RE = re.compile( r'\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}' )


def _flatten_string_values(
      values: dict[ str, Any ],
      prefix: str = '' ) -> dict[ str, str ]:
   flattened = {}

   for key, value in values.items():
      path = '{}.{}'.format( prefix, key ) if prefix else key

      if isinstance( value, dict ):
         flattened.update( _flatten_string_values( value, path ) )
      else:
         flattened[ path ] = str( value )

   return flattened


def get_html_string_values() -> dict[ str, str ]:
   result = subprocess.run(
      [ 'node', STRING_EXPORT_SCRIPT ],
      check=True,
      capture_output=True,
      text=True
   )

   return _flatten_string_values( json.loads( result.stdout ) )


def render_html_strings( content: str ) -> str:
   string_values = get_html_string_values()

   def replace_token( match: re.Match[ str ] ) -> str:
      key = match.group( 1 )
      value = string_values.get( key )

      if value is None:
         return match.group( 0 )

      return html.escape( value, quote=True )

   return HTML_STRING_TOKEN_RE.sub( replace_token, content )
