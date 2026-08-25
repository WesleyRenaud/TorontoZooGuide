from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any


STRING_EXPORT_SCRIPT = Path( './tools/exportStringValues.mjs' )
STRING_SOURCE_FILES = (
   STRING_EXPORT_SCRIPT,
   Path( './scripts/strings.js' ),
   Path( './scripts/strings/guestStatus.js' ),
   Path( './scripts/strings/common.js' ),
   Path( './scripts/strings/itinerary.js' ),
   Path( './scripts/strings/map.js' ),
   Path( './scripts/strings/console.js' ),
   Path( './scripts/strings/pages.js' ),
)

_cached_mtime: float | None = None
_cached_values: dict[ str, str ] | None = None


def _flatten_string_values(
      values: dict[ str, Any ],
      prefix: str = '' ) -> dict[ str, str ]:
   flattened: dict[ str, str ] = {}

   for key, value in values.items():
      path = '{}.{}'.format( prefix, key ) if prefix else key

      if isinstance( value, dict ):
         flattened.update( _flatten_string_values( value, path ) )
      else:
         flattened[ path ] = str( value )

   return flattened


def _string_source_mtime() -> float:
   return max( source.stat().st_mtime for source in STRING_SOURCE_FILES )


def clear_app_string_cache() -> None:
   global _cached_mtime, _cached_values

   _cached_mtime = None
   _cached_values = None


def get_app_string_values() -> dict[ str, str ]:
   global _cached_mtime, _cached_values

   mtime = _string_source_mtime()

   if _cached_values is not None and _cached_mtime == mtime:
      return _cached_values

   result = subprocess.run(
      [ 'node', str( STRING_EXPORT_SCRIPT ) ],
      check=True,
      capture_output=True,
      text=True )
   values = _flatten_string_values( json.loads( result.stdout ) )

   _cached_mtime = mtime
   _cached_values = values

   return values


def format_app_string( key: str, **params: object ) -> str:
   template = get_app_string_values().get( key )

   if template is None:
      raise KeyError( 'Unknown app string key: {}'.format( key ) )

   return template.format( **params )
