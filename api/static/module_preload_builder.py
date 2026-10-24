from __future__ import annotations

import os
import re
from typing import ClassVar


class ModulePreloadBuilder():
   MODULE_SCRIPT_RE: ClassVar[ re.Pattern[ str ] ] = re.compile(
      r'<script\b(?=[^>]*\btype="module")(?=[^>]*\bsrc="([^"]+)")[^>]*>\s*</script>',
      re.IGNORECASE,
   )
   IMPORT_RE: ClassVar[ re.Pattern[ str ] ] = re.compile(
      r'''(?:\bfrom\s*|\bimport\s*(?:\(\s*)?)['"](\.[^'"]+)['"]''',
   )
   graphs: ClassVar[ dict[ str, tuple[ list[ tuple[ float, int ] ], list[ str ] ] ] ] = {}


   @classmethod
   def clear_cache( cls ) -> None:
      cls.graphs.clear()


   @classmethod
   def inject(
         cls,
         content: str,
         filepath: str ) -> str:
      match = cls.MODULE_SCRIPT_RE.search( content )

      if match is None:
         return content

      entry = os.path.normpath( os.path.join( os.path.dirname( filepath ), match.group( 1 ) ) )
      urls = cls.urls_for_entry( entry )

      if not urls:
         return content

      line_start = content.rfind( '\n', 0, match.start() ) + 1
      indent = content[ line_start:match.start() ]

      if indent.strip() != '':
         indent = ''

      links = '\n'.join(
         f'{ indent }<link rel="modulepreload" href="{ url }">'
         for url in urls
      )

      return f'{ content[ :match.start() ] }{ links }\n{ content[ match.start(): ] }'


   @classmethod
   def urls_for_entry( cls, entry_path: str ) -> list[ str ]:
      abs_entry = os.path.abspath( entry_path )

      if not os.path.isfile( abs_entry ):
         return []

      files = cls._collect( abs_entry )
      signature = [
         ( os.path.getmtime( file_path ), os.path.getsize( file_path ) )
         for file_path in files
      ]
      cached = cls.graphs.get( abs_entry )

      if cached is not None and cached[ 0 ] == signature:
         return cached[ 1 ]

      urls = [ cls._url_for( file_path ) for file_path in files ]
      cls.graphs[ abs_entry ] = ( signature, urls )

      return urls


   @classmethod
   def _collect( cls, abs_entry: str ) -> list[ str ]:
      seen: set[ str ] = set()
      pending = [ abs_entry ]

      while pending:
         file_path = pending.pop()

         if file_path in seen or not os.path.isfile( file_path ):
            continue

         seen.add( file_path )

         with open( file_path, encoding='utf-8' ) as handle:
            source = handle.read()

         for match in cls.IMPORT_RE.finditer( source ):
            imported = os.path.normpath( os.path.join( os.path.dirname( file_path ), match.group( 1 ) ) )

            if not imported.endswith( '.js' ):
               imported = f'{ imported }.js'

            pending.append( imported )

      return sorted( seen )


   @classmethod
   def _url_for( cls, file_path: str ) -> str:
      relative = os.path.relpath( file_path, os.getcwd() ).replace( os.sep, '/' )

      return f'/{ relative }'
