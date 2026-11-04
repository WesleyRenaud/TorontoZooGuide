from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from email.message import EmailMessage
from html import escape
import os
from pathlib import Path
import re
import smtplib
import subprocess
import sys
import tempfile


SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'wesleyrenaud736@gmail.com'
PASSWORD_VARIABLE = 'CHECK_EMAIL_PASSWORD'
ROOT = Path( __file__ ).resolve().parents[ 1 ]
HEADER_RE = re.compile(
   r'^(?P<kind>.+) check for (?P<day>\d{4}-\d{2}-\d{2})\.(?: (?P<note>.*))?$'
)
CATEGORY_RE = re.compile( r'^(?P<title>[^ ].*): (?P<count>\d+)$' )
COUNT_LINE_RE = re.compile( r'^\d+ for encounters, ' )
FONT = "'Poppins', 'Segoe UI', Helvetica, Arial, sans-serif"
GREEN = '#5e9600'
GREEN_DARK = '#4b7c00'
GREEN_MUTED = '#53841c'
GREEN_HIGHLIGHT = '#77b800'
LEAF_EDGE = '#d5d8ce'
TEXT = '#141d0a'
PANEL = '#e2e8d4'
WHITE = '#ffffff'
DANGER = '#c2412d'
DANGER_SOFT = '#fde8e4'
SECTION_NAMES = {
   'Wild encounter schedule': 'Encounters',
   'Guardians talk schedule': 'Guardians Talks',
   'Seasonal off-display': 'Animals off display',
   'Seasonal attraction closure': 'Attractions closed for the season',
   'Seasonal restaurant closure': 'Restaurants closed for the season',
   'Seasonal gift shop closure': 'Gift shops closed for the season',
   'Seasonal drinking fountain closure': 'Drinking fountains closed for the season',
   'Animal list': 'Animal list',
   'Attraction list': 'Attraction list',
   'Restaurant list': 'Restaurant list',
   'Gift shop list': 'Gift shop list',
   'Zoo hours': 'Zoo hours',
}


@dataclass
class DetailItem:
   title: str
   details: list[ str ]


@dataclass
class Category:
   title: str
   count: int
   items: list[ DetailItem ]


@dataclass
class Section:
   kind: str
   day: str
   note: str
   categories: list[ Category ]


@dataclass
class Report:
   sections: list[ Section ]
   counts: list[ tuple[ str, int ] ]
   errors: str | None


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Email the daily Toronto Zoo website check summary, or open a local '
         'preview of that message.'
      )
   )
   parser.add_argument(
      '--preview',
      action='store_true',
      help='Write the email and open it locally. Does not send mail.',
   )
   parser.add_argument(
      '--output',
      type=Path,
      help='File containing the check output. The preview runs the check when this is omitted.',
   )
   parser.add_argument(
      '--exit-code',
      type=int,
      help='Exit code from the check. Required with --output.',
   )
   parser.add_argument(
      '--html',
      type=Path,
      help='Where to write the preview. Defaults to a file in the temp directory.',
   )
   return parser.parse_args()


def summary_line( body: str ) -> str | None:
   for line in reversed( body.splitlines() ):
      stripped = line.strip()

      if stripped == '1 error':
         return stripped

      count = stripped.removesuffix( ' errors' )

      if count.isdigit() and f'{ count } errors' == stripped:
         return stripped

   return None


def subject_for( body: str, exit_code: int ) -> str:
   if exit_code == 0 or exit_code == 1:
      line = summary_line( body )

      if line is not None:
         return f'Toronto Zoo check: { line }'

      return 'Toronto Zoo check finished'

   return 'Toronto Zoo check could not finish'


def parse_counts( line: str ) -> list[ tuple[ str, int ] ]:
   counts = []

   for part in line.split( ', ' ):
      count_text, separator, label = part.partition( ' for ' )

      if separator == '' or not count_text.isdigit():
         continue

      name = label.removeprefix( 'the ' )
      counts.append( ( f'{ name[ :1 ].upper() }{ name[ 1: ] }', int( count_text ) ) )

   return counts


def section_name( kind: str ) -> str:
   return SECTION_NAMES.get( kind, kind )


def format_day( day: str ) -> str:
   parsed = date.fromisoformat( day )
   return f'{ parsed.strftime( "%A" ) }, { parsed.strftime( "%B" ) } { parsed.day }, { parsed.year }'


def parse_report( body: str ) -> Report:
   sections: list[ Section ] = []
   counts: list[ tuple[ str, int ] ] = []
   errors = summary_line( body )
   current: Section | None = None
   category: Category | None = None
   item: DetailItem | None = None

   def finish_category() -> None:
      nonlocal category, item

      if current is not None and category is not None:
         current.categories.append( category )

      category = None
      item = None

   def finish_section() -> None:
      nonlocal current

      finish_category()

      if current is not None:
         sections.append( current )

      current = None

   for raw_line in body.splitlines():
      stripped = raw_line.strip()

      if COUNT_LINE_RE.match( stripped ):
         counts = parse_counts( stripped )
         finish_section()
         continue

      if errors is not None and stripped == errors and current is None:
         continue

      header = HEADER_RE.match( stripped )

      if header is not None:
         finish_section()
         current = Section(
            header.group( 'kind' ),
            header.group( 'day' ),
            header.group( 'note' ) or '',
            [],
         )
         category = None
         item = None
         continue

      if current is None or stripped == '':
         continue

      category_match = CATEGORY_RE.match( raw_line )

      if category_match is not None:
         finish_category()
         category = Category(
            category_match.group( 'title' ),
            int( category_match.group( 'count' ) ),
            [],
         )
         item = None
         continue

      if category is None:
         if current.note == '':
            current.note = stripped
         else:
            current.note = f'{ current.note } { stripped }'

         continue

      if raw_line.startswith( '    ' ):
         if item is None:
            item = DetailItem( stripped, [] )
            category.items.append( item )
         else:
            item.details.append( stripped )

         continue

      item = DetailItem( stripped, [] )
      category.items.append( item )

   finish_section()
   return Report( sections, counts, errors )


def text( value: str ) -> str:
   return escape( value, quote=True )


def cell( content: str, style: str, attributes: str = '' ) -> str:
   extra = f' { attributes }' if attributes else ''
   return f'<td style="{ style }"{ extra }>{ content }</td>'


def status_copy( exit_code: int, errors: str | None ) -> tuple[ str, str, str ]:
   if exit_code == 2 or errors is None:
      return DANGER, 'Could not finish', 'The check did not finish.'

   if errors == '0 errors':
      return GREEN, 'All clear', 'The website and the app match.'

   return DANGER, errors, 'These checks differ from the website.'


def count_cell( label: str, count: int ) -> str:
   clear = count == 0
   number_color = GREEN if clear else DANGER
   background = WHITE if clear else DANGER_SOFT
   edge = LEAF_EDGE if clear else DANGER
   label_color = TEXT
   label_cell = cell(
      text( label ),
      (
         f'padding:14px 8px 14px 16px;font-family:{ FONT };font-size:13px;'
         f'line-height:18px;font-weight:500;color:{ label_color };'
      ),
   )
   number_cell = cell(
      text( str( count ) ),
      (
         f'padding:10px 16px 10px 8px;font-family:{ FONT };font-size:26px;'
         f'line-height:30px;font-weight:700;color:{ number_color };text-align:right;'
      ),
      'align="right"',
   )
   inner = (
      f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
      f'style="background:{ background };border:1px solid { edge };border-radius:10px;">'
      f'<tr>{ label_cell }{ number_cell }</tr></table>'
   )
   return cell( inner, 'padding:6px;vertical-align:top;', 'width="50%"' )


def count_grid( counts: list[ tuple[ str, int ] ] ) -> str:
   if not counts:
      return ''

   rows = []
   pair = counts[ : ]

   if len( pair ) % 2 == 1:
      pair.append( ( '', -1 ) )

   for index in range( 0, len( pair ), 2 ):
      left_label, left_count = pair[ index ]
      right_label, right_count = pair[ index + 1 ]
      left = count_cell( left_label, left_count )
      right = (
         cell( '', 'padding:6px;', 'width="50%"' )
         if right_count < 0
         else count_cell( right_label, right_count )
      )
      rows.append( f'<tr>{ left }{ right }</tr>' )

   return (
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
      f'style="margin-top:8px;">{ "".join( rows ) }</table>'
   )


def detail_text( detail: str ) -> str:
   label, separator, value = detail.partition( ': ' )

   if not separator:
      return text( detail )

   return (
      f'<span style="font-weight:600;color:{ GREEN };">{ text( label ) }</span>'
      f'{ separator }{ text( value ) }'
   )


def detail_rows( item: DetailItem ) -> str:
   rows = [
      cell(
         text( item.title ),
         (
            f'padding:4px 20px 2px 32px;font-family:{ FONT };font-size:16px;'
            f'line-height:22px;font-weight:700;color:{ TEXT };'
         ),
      )
   ]

   for detail in item.details:
      rows.append(
         cell(
            detail_text( detail ),
            (
               f'padding:1px 20px 1px 44px;font-family:{ FONT };font-size:13px;'
               f'line-height:18px;color:{ GREEN_MUTED };'
            ),
         )
      )

   return ''.join( f'<tr>{ row }</tr>' for row in rows )


def category_block( category: Category ) -> str:
   number_color = GREEN if category.count == 0 else DANGER
   title_cell = cell(
      text( category.title ),
      (
         f'padding:12px 8px 2px 20px;font-family:{ FONT };font-size:14px;'
         f'line-height:20px;font-weight:500;color:{ GREEN_DARK };'
      ),
   )
   count_badge = cell(
      text( str( category.count ) ),
      (
         f'padding:10px 20px 2px 8px;font-family:{ FONT };font-size:18px;'
         f'line-height:22px;font-weight:700;color:{ number_color };text-align:right;'
      ),
      'align="right"',
   )
   rows = [ f'<tr>{ title_cell }{ count_badge }</tr>' ]
   rows.extend( detail_rows( item ) for item in category.items )
   return ''.join( rows )


def section_card( section: Section ) -> str:
   title = cell(
      text( section_name( section.kind ) ),
      (
         f'padding:12px 20px;font-family:{ FONT };font-size:18px;'
         f'line-height:24px;font-weight:700;color:{ WHITE };background:{ GREEN_MUTED };'
      ),
   )
   rows = [ f'<tr>{ title }</tr>' ]

   if section.categories:
      rows.append(
         '<tr><td style="padding:0 0 12px;">'
         '<table role="presentation" width="100%" cellpadding="0" cellspacing="0">'
         + ''.join( category_block( category ) for category in section.categories )
         + '</table></td></tr>'
      )

   return (
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
      f'style="margin-top:16px;background:{ WHITE };border-radius:12px;'
      f'border:1px solid { LEAF_EDGE };">'
      + ''.join( rows )
      + '</table>'
   )


def notable_sections( report: Report ) -> list[ Section ]:
   notable = []

   for section in report.sections:
      has_issue = any( category.count > 0 for category in section.categories )

      if has_issue:
         notable.append( section )

   return notable


def message_card( message: str ) -> str:
   return (
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
      f'style="margin-top:16px;background:{ WHITE };border-radius:12px;'
      f'border:1px solid { LEAF_EDGE };border-left:6px solid { GREEN };">'
      '<tr>'
      + cell(
         text( message ),
         (
            f'padding:18px 20px;font-family:{ FONT };font-size:15px;'
            f'line-height:22px;font-weight:400;color:{ TEXT };'
         ),
      )
      + '</tr></table>'
   )


def render_html( body: str, exit_code: int ) -> str:
   report = parse_report( body )
   day = report.sections[ 0 ].day if report.sections else ''
   headline_color, headline, summary = status_copy( exit_code, report.errors )
   date_line = ''

   if day:
      date_line = (
         '<tr>'
         + cell(
            text( format_day( day ) ),
            (
               f'padding:4px 24px 22px;font-family:{ FONT };font-size:14px;'
               f'line-height:20px;font-weight:400;color:{ WHITE };'
            ),
         )
         + '</tr>'
      )
   sections = notable_sections( report )
   detail = ''.join( section_card( section ) for section in sections )

   if not report.sections and body.strip():
      detail = message_card( body.strip() )

   status = (
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
      f'style="background:{ WHITE };border-top:4px solid { GREEN_HIGHLIGHT };'
      f'border-radius:0 0 12px 12px;">'
      '<tr>'
      + cell(
         text( headline ),
         (
            f'padding:20px 24px 2px;font-family:{ FONT };font-size:30px;'
            f'line-height:36px;font-weight:700;color:{ headline_color };'
         ),
      )
      + '</tr><tr>'
      + cell(
         text( summary ),
         (
            f'padding:0 24px 20px;font-family:{ FONT };font-size:15px;'
            f'line-height:22px;font-weight:400;color:{ TEXT };'
         ),
      )
      + '</tr></table>'
   )
   header = (
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
      f'style="background:{ GREEN };border-radius:12px 12px 0 0;">'
      '<tr>'
      + cell(
         'Toronto Zoo Guide',
         (
            f'padding:26px 24px 0;font-family:{ FONT };font-size:12px;'
            f'line-height:16px;font-weight:600;letter-spacing:0.14em;'
            f'text-transform:uppercase;color:{ WHITE };'
         ),
      )
      + '</tr><tr>'
      + cell(
         'Daily website check',
         (
            f'padding:{ "6px 24px 2px" if day else "6px 24px 24px" };font-family:{ FONT };'
            f'font-size:26px;line-height:32px;font-weight:700;color:{ WHITE };'
         ),
      )
      + '</tr>'
      + date_line
      + '</table>'
   )
   content = f'{ header }{ status }{ count_grid( report.counts ) }{ detail }'
   shell = (
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
      f'style="background:{ PANEL };">'
      '<tr><td align="center" style="padding:24px 12px;">'
      '<table role="presentation" width="600" cellpadding="0" cellspacing="0" '
      'style="width:100%;max-width:600px;">'
      f'<tr><td>{ content }</td></tr>'
      '</table></td></tr></table>'
   )
   return (
      '<!DOCTYPE html><html><head><meta charset="utf-8"></head>'
      f'<body style="margin:0;padding:0;background:{ PANEL };">{ shell }</body></html>'
   )


def run_check() -> tuple[ str, int ]:
   result = subprocess.run(
      [ sys.executable, '-m', 'tools.scheduleCheck' ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
   )
   return f'{ result.stdout }{ result.stderr }', result.returncode


def preview_path( requested: Path | None ) -> Path:
   if requested is not None:
      return requested

   return Path( tempfile.gettempdir() ) / 'toronto-zoo-check-email.html'


def open_preview( path: Path ) -> None:
   command = [ 'open', str( path ) ]

   if sys.platform != 'darwin':
      command = [ 'xdg-open', str( path ) ]

   subprocess.run( command, check=False )


def write_preview( body: str, exit_code: int, path: Path ) -> None:
   path.write_text( render_html( body, exit_code ) )


def preview( args: argparse.Namespace ) -> int:
   if args.output is None:
      body, exit_code = run_check()
   else:
      if args.exit_code is None:
         print( 'Pass --exit-code with --output.', file=sys.stderr )
         return 2

      if not args.output.exists():
         print( f'Could not find { args.output }.', file=sys.stderr )
         return 2

      body = args.output.read_text()
      exit_code = args.exit_code

   if body.strip() == '':
      body = 'The check produced no output.'

   path = preview_path( args.html )
   write_preview( body, exit_code, path )
   open_preview( path )
   print( path )
   return 0


def send_summary( body: str, exit_code: int, password: str ) -> None:
   message = EmailMessage()
   message[ 'Subject' ] = subject_for( body, exit_code )
   message[ 'From' ] = EMAIL_ADDRESS
   message[ 'To' ] = EMAIL_ADDRESS
   message.set_content( body )
   message.add_alternative( render_html( body, exit_code ), subtype='html' )
   server = smtplib.SMTP( SMTP_HOST, SMTP_PORT, timeout=30 )

   try:
      server.ehlo()
      server.starttls()
      server.ehlo()
      server.login( EMAIL_ADDRESS, password )
      server.send_message( message )
   finally:
      server.quit()


def main() -> int:
   args = parse_args()

   if args.preview:
      return preview( args )

   if args.output is None or args.exit_code is None:
      print( 'Pass --output and --exit-code, or use --preview.', file=sys.stderr )
      return 2

   password = os.environ.get( PASSWORD_VARIABLE, '' )

   if password == '':
      print(
         f'Set the { PASSWORD_VARIABLE } secret to a Gmail app password.',
         file=sys.stderr,
      )
      return 2

   if not args.output.exists():
      print( f'Could not find { args.output }.', file=sys.stderr )
      return 2

   body = args.output.read_text()

   if body.strip() == '':
      body = 'The check produced no output.'

   try:
      send_summary( body, args.exit_code, password )
   except OSError as error:
      print( error, file=sys.stderr )
      return 2

   return 0


if __name__ == '__main__':
   raise SystemExit( main() )
