from __future__ import annotations

import ast
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath
import re
import sys
import tomllib
from typing import Any


def find_root() -> Path:
   current = Path( __file__ ).resolve().parent

   while current != current.parent:
      if ( current / 'pyproject.toml' ).exists():
         return current

      current = current.parent

   return Path( __file__ ).resolve().parents[ 2 ]


ROOT = find_root()


def get_display_path( path: Path ) -> str:
   try:
      return path.relative_to( ROOT ).as_posix()

   except ValueError:
      return path.as_posix()


def load_config() -> dict[ str, Any ]:
   pyproject_path = ROOT / 'pyproject.toml'

   if not pyproject_path.exists():
      return {}

   return (
      tomllib.loads( pyproject_path.read_text() )
      .get( 'tool', {} )
      .get( 'tzg_python_one_class_per_file', {} )
   )


def snake_to_pascal( stem: str ) -> str:
   return ''.join( word.capitalize() for word in stem.split( '_' ) )


def is_excluded_path( path: Path, patterns: list[ str ] ) -> bool:
   display_path = get_display_path( path )

   for pattern in patterns:
      if PurePosixPath( display_path ).match( pattern ):
         return True

      if fnmatch( display_path, pattern ):
         return True

   return False


def class_names( path: Path ) -> list[ str ]:
   try:
      tree = ast.parse( path.read_text() )
   except SyntaxError as error:
      raise ValueError( f'{ get_display_path( path ) }: { error }' ) from error

   return [
      node.name
      for node in tree.body
      if isinstance( node, ast.ClassDef )
   ]


def check_file( path: Path ) -> list[ str ]:
   classes = class_names( path )
   expected = snake_to_pascal( path.stem )
   display_path = get_display_path( path )
   violations: list[ str ] = []

   if len( classes ) == 0:
      violations.append(
         f'{ display_path }: expected exactly one class named { expected }, found none' )
      return violations

   if len( classes ) > 1:
      violations.append(
         f'{ display_path }: expected exactly one class, found { len( classes ) }: { ", ".join( classes ) }' )
      return violations

   if classes[ 0 ] != expected:
      violations.append(
         f'{ display_path }: class { classes[ 0 ] } must match file name { expected }' )

   return violations


def iter_python_files( include: list[ str ] ) -> list[ Path ]:
   paths: set[ Path ] = set()

   for pattern in include:
      paths.update( ROOT.glob( pattern ) )

   return sorted( paths )


def main() -> int:
   config = load_config()
   include = config.get( 'include', [ 'api/**/*.py' ] )
   violations: list[ str ] = []

   for path in iter_python_files( include ):
      if path.name in ( '__init__.py', '__main__.py' ):
         continue

      try:
         violations.extend( check_file( path ) )
      except ValueError as error:
         violations.append( str( error ) )

   if not violations:
      return 0

   for violation in violations:
      print( violation )

   print( f'\nFound { len( violations ) } one-class-per-file violation(s).' )
   return 1


if __name__ == '__main__':
   sys.exit( main() )
