from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any


class AppStringProvider():
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


   @classmethod
   def clear_cache( cls ) -> None:
      cls._cached_mtime = None
      cls._cached_values = None


   @classmethod
   def values( cls ) -> dict[ str, str ]:
      mtime = cls._string_source_mtime()

      if cls._cached_values is not None and cls._cached_mtime == mtime:
         return cls._cached_values

      result = subprocess.run(
         [ 'node', str( cls.STRING_EXPORT_SCRIPT ) ],
         check=True,
         capture_output=True,
         text=True )
      values = cls._flatten_string_values( json.loads( result.stdout ) )

      cls._cached_mtime = mtime
      cls._cached_values = values

      return values


   @classmethod
   def format(
         cls,
         key: str,
         **params: object ) -> str:
      template = cls.values().get( key )

      if template is None:
         raise KeyError( 'Unknown app string key: {}'.format( key ) )

      return template.format( **params )


   @classmethod
   def _flatten_string_values(
         cls,
         values: dict[ str, Any ],
         prefix: str = '' ) -> dict[ str, str ]:
      flattened: dict[ str, str ] = {}

      for key, value in values.items():
         path = '{}.{}'.format( prefix, key ) if prefix else key

         if isinstance( value, dict ):
            flattened.update( cls._flatten_string_values( value, path ) )
         else:
            flattened[ path ] = str( value )

      return flattened


   @classmethod
   def _string_source_mtime( cls ) -> float:
      return max( source.stat().st_mtime for source in cls.STRING_SOURCE_FILES )
