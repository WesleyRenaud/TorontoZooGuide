from __future__ import annotations

import html
import json
from pathlib import Path
import re
import subprocess
from typing import Any


STRING_EXPORT_SCRIPT = './tools/exportStringValues.mjs'
STRING_SOURCE_FILES = (
   Path( STRING_EXPORT_SCRIPT ),
   Path( './scripts/strings.js' ),
)
HTML_STRING_TOKEN_RE = re.compile( r'\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}' )

_cached_mtime: float | None = None
_cached_values: dict[ str, str ] | None = None


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


def _string_source_mtime() -> float:
   return max( source.stat().st_mtime for source in STRING_SOURCE_FILES )


def clear_html_string_cache() -> None:
   global _cached_mtime, _cached_values

   _cached_mtime = None
   _cached_values = None


def get_html_string_values() -> dict[ str, str ]:
   global _cached_mtime, _cached_values

   mtime = _string_source_mtime()

   if _cached_values is not None and _cached_mtime == mtime:
      return _cached_values

   result = subprocess.run(
      [ 'node', STRING_EXPORT_SCRIPT ],
      check=True,
      capture_output=True,
      text=True
   )
   values = _flatten_string_values( json.loads( result.stdout ) )

   _cached_mtime = mtime
   _cached_values = values

   return values


def render_html_strings( content: str ) -> str:
   string_values = get_html_string_values()

   def replace_token( match: re.Match[ str ] ) -> str:
      key = match.group( 1 )
      value = string_values.get( key )

      if value is None:
         return match.group( 0 )

      return html.escape( value, quote=True )

   return HTML_STRING_TOKEN_RE.sub( replace_token, content )
