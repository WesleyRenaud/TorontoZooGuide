import ast
from pathlib import Path
from io import BytesIO
from fnmatch import fnmatch
import sys
import tokenize
import tomllib


def find_root():
   current = Path( __file__ ).resolve().parent

   while current != current.parent:
      if ( current / 'pyproject.toml' ).exists():
         return current

      current = current.parent

   return Path( __file__ ).resolve().parents[ 2 ]


ROOT = find_root()
SKIP_TOKEN_TYPES = {
   tokenize.NL,
   tokenize.NEWLINE,
   tokenize.INDENT,
   tokenize.DEDENT,
   tokenize.COMMENT,
   tokenize.ENCODING
}
OPENERS = {
   '(': ')',
   '[': ']',
   '{': '}'
}
CLOSERS = {
   ')': '(',
   ']': '[',
   '}': '{'
}


def get_display_path( path ):
   try:
      return path.relative_to( ROOT ).as_posix()

   except ValueError:
      return path.as_posix()


def load_style_config():
   pyproject_path = ROOT / 'pyproject.toml'

   if not pyproject_path.exists():
      return {}

   return (
      tomllib.loads( pyproject_path.read_text() )
      .get( 'tool', {} )
      .get( 'tzg_python_style', {} )
   )


def get_definition_start_line( node ):
   if getattr( node, 'decorator_list', None ):
      return min( decorator.lineno for decorator in node.decorator_list )

   return node.lineno


def check_method_spacing( path, file_text, blank_lines_between_methods ):
   try:
      tree = ast.parse( file_text )
   except SyntaxError:
      return []

   lines = file_text.splitlines()
   violations = []

   for node in ast.walk( tree ):
      if not isinstance( node, ast.ClassDef ):
         continue

      methods = [
         item
         for item in node.body
         if isinstance( item, ( ast.FunctionDef, ast.AsyncFunctionDef ) )
      ]

      for previous, current in zip( methods, methods[ 1: ] ):
         previous_end_line = previous.end_lineno or previous.lineno
         current_start_line = get_definition_start_line( current )
         blank_line_count = 0

         for line_number in range( previous_end_line + 1, current_start_line ):
            if lines[ line_number - 1 ].strip() == '':
               blank_line_count += 1

         if blank_line_count == blank_lines_between_methods:
            continue

         add_violation(
            violations,
            path,
            current_start_line,
            1,
            (
               f'Expected { blank_lines_between_methods } blank lines between method '
               f'definitions, found { blank_line_count }.'
            )
         )

   return violations


def is_excluded_path( path, excluded_patterns ):
   relative_path = path.relative_to( ROOT ).as_posix()

   if any( part in { '.git', '__pycache__', 'node_modules' } for part in path.parts ):
      return True

   for pattern in excluded_patterns:
      if fnmatch( relative_path, pattern ):
         return True

   return False


def get_significant_token( tokens, start_index, step ):
   index = start_index

   while 0 <= index < len( tokens ):
      token = tokens[ index ]

      if token.type not in SKIP_TOKEN_TYPES:
         return token

      index += step

   return None


def add_violation( violations, path, line, column, message ):
   violations.append( ( get_display_path( path ), line, column, message ) )


def build_char_positions( text, start ):
   line, column = start
   positions = []

   for character in text:
      positions.append( ( line, column ) )

      if character == '\n':
         line += 1
         column = 0

      else:
         column += 1

   return positions


def check_opening_spacing( violations, path, positions, text, index ):
   if index + 1 >= len( text ):
      return

   next_character = text[ index + 1 ]

   if next_character == OPENERS[ text[ index ] ] or next_character.isspace():
      return

   line, column = positions[ index ]
   add_violation(
      violations,
      path,
      line,
      column + 1,
      f'Missing space after "{ text[ index ] }".'
   )


def check_closing_spacing( violations, path, positions, text, index ):
   if index == 0:
      return

   previous_character = text[ index - 1 ]

   if previous_character == CLOSERS[ text[ index ] ] or previous_character.isspace():
      return

   line, column = positions[ index ]
   add_violation(
      violations,
      path,
      line,
      column + 1,
      f'Missing space before "{ text[ index ] }".'
   )


def skip_string_literal( text, index ):
   quote_character = text[ index ]
   is_triple_quoted = text[ index:index + 3 ] == quote_character * 3

   if is_triple_quoted:
      index += 3

      while index < len( text ):
         if text[ index ] == '\\':
            index += 2
            continue

         if text[ index:index + 3 ] == quote_character * 3:
            return index + 3

         index += 1

      return len( text )

   index += 1

   while index < len( text ):
      if text[ index ] == '\\':
         index += 2
         continue

      if text[ index ] == quote_character:
         return index + 1

      index += 1

   return len( text )


def is_f_string_token( token_string ):
   prefix = []
   index = 0

   while index < len( token_string ) and token_string[ index ].isalpha():
      prefix.append( token_string[ index ] )
      index += 1

   return 'f' in ''.join( prefix ).lower()


def check_f_string_field( violations, path, positions, text, start_index ):
   stack = [ '{' ]
   index = start_index

   while index < len( text ):
      character = text[ index ]

      if character in { "'", '"' }:
         index = skip_string_literal( text, index )
         continue

      if character in OPENERS:
         check_opening_spacing( violations, path, positions, text, index )
         stack.append( character )
         index += 1
         continue

      if character in CLOSERS:
         check_closing_spacing( violations, path, positions, text, index )

         if stack and stack[ -1 ] == CLOSERS[ character ]:
            stack.pop()
            index += 1

            if not stack:
               return index

            continue

      index += 1

   return index


def check_f_string_token( path, token ):
   if token.type != tokenize.STRING or not is_f_string_token( token.string ):
      return []

   positions = build_char_positions( token.string, token.start )
   violations = []
   index = 0

   while index < len( token.string ):
      if token.string[ index ] != '{':
         index += 1
         continue

      if index + 1 < len( token.string ) and token.string[ index + 1 ] == '{':
         index += 2
         continue

      check_opening_spacing( violations, path, positions, token.string, index )
      index = check_f_string_field( violations, path, positions, token.string, index + 1 )

   return violations


def check_file( path, blank_lines_between_methods ):
   file_text = path.read_text()
   tokens = [
      token
      for token in tokenize.tokenize( BytesIO( file_text.encode() ).readline )
      if token.type != tokenize.ENDMARKER
   ]
   violations = check_method_spacing( path, file_text, blank_lines_between_methods )

   for index, token in enumerate( tokens ):
      if token.type == tokenize.STRING:
         violations.extend( check_f_string_token( path, token ) )
         continue

      if token.type != tokenize.OP:
         continue

      if token.string in OPENERS:
         next_token = get_significant_token( tokens, index + 1, 1 )

         if next_token == None:
            continue

         if next_token.type == tokenize.OP and next_token.string == OPENERS[ token.string ]:
            continue

         if next_token.start[ 0 ] == token.end[ 0 ] and next_token.start[ 1 ] == token.end[ 1 ]:
            add_violation(
               violations,
               path,
               token.start[ 0 ],
               token.start[ 1 ] + 1,
               f'Missing space after "{ token.string }".'
            )

      elif token.string in CLOSERS:
         previous_token = get_significant_token( tokens, index - 1, -1 )

         if previous_token == None:
            continue

         if previous_token.type == tokenize.OP and previous_token.string == CLOSERS[ token.string ]:
            continue

         if previous_token.end[ 0 ] == token.start[ 0 ] and previous_token.end[ 1 ] == token.start[ 1 ]:
            add_violation(
               violations,
               path,
               token.start[ 0 ],
               token.start[ 1 ] + 1,
               f'Missing space before "{ token.string }".'
            )

   return violations


def main():
   style_config = load_style_config()
   excluded_patterns = style_config.get( 'exclude', [] )
   blank_lines_between_methods = style_config.get( 'blank_lines_between_methods', 2 )
   violations = []

   for path in sorted( ROOT.rglob( '*.py' ) ):
      if is_excluded_path( path, excluded_patterns ):
         continue

      violations.extend( check_file( path, blank_lines_between_methods ) )

   if not violations:
      return 0

   for path, line, column, message in violations:
      print( f'{ path }:{ line }:{ column }: { message }' )

   print( f'\nFound { len( violations ) } Python house-style violation(s).' )

   return 1


if __name__ == '__main__':
   sys.exit( main() )
