from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
import re
import sys


ROOT = Path( __file__ ).resolve().parents[ 1 ]
CATALOG_PATH = ROOT / 'shared' / 'enums' / 'catalog.json'

if str( ROOT ) not in sys.path:
   sys.path.insert( 0, str( ROOT ) )


def load_catalog() -> dict:
   return json.loads( CATALOG_PATH.read_text( encoding='utf-8' ) )


def load_json_members( json_name: str ) -> dict[ str, str | int ]:
   path = ROOT / 'shared' / 'enums' / json_name
   members = json.loads( path.read_text( encoding='utf-8' ) )

   if not isinstance( members, dict ) or not members:
      raise ValueError( f'{ path }: expected a non-empty object' )

   return dict( sorted( members.items() ) )


def python_module_name( relative_path: str ) -> str:
   return relative_path.removesuffix( '.py' ).replace( '/', '.' )


def has_object_values( entry: dict, members: dict ) -> bool:
   if entry.get( 'valueShape' ) == 'object':
      return True

   return all( isinstance( value, dict ) for value in members.values() )


def check_object_members( entry: dict, members: dict ) -> list[ str ]:
   violations: list[ str ] = []
   location = f'shared/enums/{ entry[ "json" ] }'

   for name, value in members.items():
      if not isinstance( value, dict ):
         violations.append( f'{ location }: { name } must be an object' )
         continue

      unknown_fields = sorted( set( value ) - { 'kind', 'itemType' } )

      if unknown_fields:
         violations.append(
            f'{ location }: unknown field(s) for { name }: '
            f'{ ", ".join( unknown_fields ) }'
         )

      if not isinstance( value.get( 'kind' ), str ) or not value[ 'kind' ]:
         violations.append(
            f'{ location }: kind for { name } must be a non-empty string'
         )

      if 'itemType' not in value:
         continue

      if not isinstance( value[ 'itemType' ], str ) or not value[ 'itemType' ]:
         violations.append(
            f'{ location }: itemType for { name } must be a non-empty string'
         )

   return violations


def expected_kinds( members: dict ) -> dict[ str, str ]:
   return { name: value[ 'kind' ] for name, value in members.items() }


def expected_item_types( members: dict ) -> dict[ str, str ]:
   return {
      name: value[ 'itemType' ]
      for name, value in members.items()
      if 'itemType' in value
   }


def check_python( entry: dict, members: dict, object_shape: bool ) -> list[ str ]:
   violations: list[ str ] = []
   module = importlib.import_module( python_module_name( entry[ 'pythonModule' ] ) )
   enum_cls = getattr( module, entry[ 'pythonClass' ], None )

   if enum_cls is None:
      return [
         f'{ entry[ "pythonModule" ] }: missing { entry[ "pythonClass" ] }'
      ]

   actual = {
      name: member.value
      for name, member in enum_cls.__members__.items()
   }

   if actual != ( expected_kinds( members ) if object_shape else members ):
      violations.append(
         f'{ entry[ "pythonModule" ] }: { entry[ "pythonClass" ] } does not match '
         f'shared/enums/{ entry[ "json" ] }'
      )

   if not object_shape:
      return violations

   actual_item_types = {
      name: member.item_type
      for name, member in enum_cls.__members__.items()
      if getattr( member, 'item_type', None ) is not None
   }

   if actual_item_types != expected_item_types( members ):
      violations.append(
         f'{ entry[ "pythonModule" ] }: { entry[ "pythonClass" ] }.item_type does not '
         f'match shared/enums/{ entry[ "json" ] }'
      )

   return violations


def check_javascript( entry: dict, members: dict ) -> list[ str ]:
   violations: list[ str ] = []
   path = ROOT / entry[ 'javascriptModule' ]
   relative = entry[ 'javascriptModule' ]

   if not path.exists():
      return [ f'missing { relative }' ]

   source = path.read_text( encoding='utf-8' )
   json_name = entry[ 'json' ]
   import_pattern = re.compile(
      rf"from\s+['\"][^'\"]*{ re.escape( json_name ) }['\"]\s+with\s*\{{\s*type:\s*['\"]json['\"]\s*\}}"
   )

   if not import_pattern.search( source ):
      violations.append(
         f'{ relative }: must import shared/enums/{ json_name } with type json'
      )

   if f'export class { entry[ "javascriptClass" ] }' not in source:
      violations.append(
         f'{ relative }: missing export class { entry[ "javascriptClass" ] }'
      )

   freeze_assign_pattern = re.compile(
      rf'{ re.escape( entry[ "javascriptClass" ] ) }\s*\[[^\]]+\]\s*=\s*Object\.freeze\('
   )

   if 'Object.assign(' not in source and not freeze_assign_pattern.search( source ):
      violations.append(
         f'{ relative }: must Object.assign shared JSON values onto the class '
         f'(or freeze-assign each member onto it)'
      )

   return violations


def report( violations: list[ str ] ) -> int:
   if not violations:
      return 0

   print( 'Shared enum check failed:' )

   for violation in violations:
      print( f'  { violation }' )

   return 1


def check() -> int:
   catalog = load_catalog()
   loaded: list[ tuple[ dict, dict, bool ] ] = []
   shape_violations: list[ str ] = []

   for entry in catalog[ 'enums' ]:
      members = load_json_members( entry[ 'json' ] )
      object_shape = has_object_values( entry, members )
      loaded.append( ( entry, members, object_shape ) )

      if object_shape:
         shape_violations.extend( check_object_members( entry, members ) )

   # Importing an API enum module runs its JSON loader, so malformed JSON has to
   # be reported before any module import is attempted.
   if shape_violations:
      return report( shape_violations )

   violations: list[ str ] = []

   for entry, members, object_shape in loaded:
      violations.extend( check_python( entry, members, object_shape ) )
      violations.extend( check_javascript( entry, members ) )

   return report( violations )


def main() -> int:
   parser = argparse.ArgumentParser(
      description=(
         'Verify API/JS shared enums load from shared/enums JSON '
         '(values are not duplicated in generated copies).'
      )
   )
   parser.parse_args()
   return check()


if __name__ == '__main__':
   raise SystemExit( main() )
