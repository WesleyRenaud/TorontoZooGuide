from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path( __file__ ).resolve().parents[ 2 ]
SEED_DATA_DIR = ROOT / 'api' / 'seed' / 'data'
ESCAPE_PATTERN = re.compile( r'\\u[0-9a-fA-F]{4}' )


def find_ascii_escapes() -> list[ str ]:
   violations: list[ str ] = []

   for path in sorted( SEED_DATA_DIR.rglob( '*.json' ) ):
      for line_number, line in enumerate( path.read_text( encoding='utf-8' ).splitlines(), start=1 ):
         if ESCAPE_PATTERN.search( line ):
            relative = path.relative_to( ROOT )
            violations.append( f'{ relative }:{ line_number }' )

   return violations


def main() -> int:
   violations = find_ascii_escapes()

   if not violations:
      return 0

   print( 'Seed JSON must use UTF-8 characters instead of \\u escapes:' )

   for violation in violations:
      print( violation )

   print( "Write JSON with json.dump( ..., ensure_ascii=False )." )
   return 1


if __name__ == '__main__':
   sys.exit( main() )
