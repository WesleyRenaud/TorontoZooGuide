from __future__ import annotations

import re

from api.app_string_provider import AppStringProvider
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .count import Count
from .report import Report
from .report_draft import ReportDraft


class CheckReportParser():
   CATEGORY_RE = re.compile( r'^(?P<title>[^ ].*): (?P<count>\d+)$' )
   COUNT_LABELS = (
      'site.nav.animals',
      'checks.countNames.exhibits',
      'map.filter.attractions',
      'site.nav.wildEncounters',
      'reports.guardiansTalk.section',
      'map.filterTypes.restaurant',
      'checks.countNames.giftShops',
      'checks.countNames.drinkingFountains',
      'reports.zooHours.kind',
   )


   @classmethod
   def header_re( cls ) -> re.Pattern[ str ]:
      values = AppStringProvider.values()
      middle = re.escape( values[ 'checks.headingMiddle' ] )
      period = re.escape( values[ 'checks.period' ] )
      return re.compile(
         rf'^(?P<kind>.+){ middle }(?P<day>\d{{4}}-\d{{2}}-\d{{2}}){ period }(?: (?P<note>.*))?$'
      )


   @classmethod
   def count_before( cls, line: str, singular: str, plural: str ) -> int | None:
      stripped = line.strip()

      if stripped == f'1{ singular }':
         return 1

      if not stripped.endswith( plural ):
         return None

      number = stripped.removesuffix( plural )

      if not number.isdigit():
         return None

      return int( number )


   @classmethod
   def error_count( cls, body: str ) -> int | None:
      lines = body.splitlines()

      if len( lines ) == 0:
         return None

      values = AppStringProvider.values()
      return cls.count_before(
         lines[ -1 ],
         values[ 'checks.error' ],
         values[ 'checks.errors' ],
      )


   @classmethod
   def format_error_count( cls, count: int ) -> str:
      suffix = 'checks.error' if count == 1 else 'checks.errors'
      return f'{ count }{ AppStringProvider.format( suffix ) }'


   @classmethod
   def format_fixed_count( cls, count: int ) -> str:
      suffix = 'checks.errorFixed' if count == 1 else 'checks.errorsFixed'
      return f'{ count }{ AppStringProvider.format( suffix ) }'


   @classmethod
   def format_detected( cls, detected: int, fixed: int ) -> str:
      suffix = 'checks.errorDetected' if detected == 1 else 'checks.errorsDetected'
      headline = f'{ detected }{ AppStringProvider.format( suffix ) }'

      if fixed == 0:
         return headline

      return headline + AppStringProvider.format( 'checks.status.detectedFixed', count=fixed )


   @classmethod
   def fixed_count( cls, line: str ) -> int | None:
      values = AppStringProvider.values()
      return cls.count_before(
         line,
         values[ 'checks.errorFixed' ],
         values[ 'checks.errorsFixed' ],
      )


   @classmethod
   def recorded_fixed_count( cls, body: str ) -> int | None:
      fixed = None

      for line in body.splitlines():
         count = cls.fixed_count( line )

         if count != None:
            fixed = count

      return fixed


   @classmethod
   def subject_for( cls, body: str, exit_code: int ) -> str:
      if exit_code == CheckExitCode.CLEAR or exit_code == CheckExitCode.DIFFERENCES:
         error_count = cls.error_count( body )

         if error_count != None:
            fixed = cls.recorded_fixed_count( body ) or 0
            return (
               AppStringProvider.format( 'checks.subject.summary' )
               + cls.format_error_count( error_count + fixed )
            )

         return AppStringProvider.format( 'checks.subject.finished' )

      return AppStringProvider.format( 'checks.subject.couldNotFinish' )


   @classmethod
   def count_marker( cls ) -> str:
      return AppStringProvider.values()[ 'checks.countItem' ]


   @classmethod
   def count_labels( cls ) -> list[ str ]:
      values = AppStringProvider.values()
      return [ values[ key ] for key in cls.COUNT_LABELS ]


   @classmethod
   def format_counts(
         cls,
         animals: int = 0,
         exhibits: int = 0,
         encounters: int = 0,
         talks: int = 0,
         attractions: int = 0,
         restaurants: int = 0,
         gift_shops: int = 0,
         drinking_fountains: int = 0,
         attraction_list: int = 0,
         zoo_hours: int = 0 ) -> str:
      counts = (
         animals,
         exhibits,
         attractions + attraction_list,
         encounters,
         talks,
         restaurants,
         gift_shops,
         drinking_fountains,
         zoo_hours,
      )
      pieces = [
         f'{ count }{ AppStringProvider.format( "checks.countItem" ) }{ label }'
         for count, label in zip( counts, cls.count_labels(), strict=True )
      ]
      return AppStringProvider.values()[ 'format.listJoin' ].join( pieces )


   @classmethod
   def count_line_re( cls ) -> re.Pattern[ str ]:
      marker = re.escape( cls.count_marker() )
      separator = re.escape( AppStringProvider.values()[ 'format.listJoin' ] )
      return re.compile( rf'^\d+{ marker }.+{ separator }' )


   @classmethod
   def parse_counts( cls, line: str ) -> list[ Count ]:
      separator = AppStringProvider.values()[ 'format.listJoin' ]
      marker = cls.count_marker()
      counts = []

      for part in line.split( separator ):
         count_text, name = part.split( marker, 1 )
         counts.append( Count( label=name, count=int( count_text ) ) )

      return counts


   @classmethod
   def parse_report( cls, body: str ) -> Report:
      draft = ReportDraft()
      error_count = cls.error_count( body )

      for raw_line in body.splitlines():
         cls.read_line( draft, raw_line )

      draft.finish_section()
      return Report( draft.sections, draft.counts, error_count, draft.fixed_count )


   @classmethod
   def read_line( cls, draft: ReportDraft, raw_line: str ) -> None:
      stripped = raw_line.strip()

      if cls.read_fixed_count( draft, stripped ):
         return

      if cls.read_counts( draft, stripped ):
         return

      if cls.read_header( draft, stripped ):
         return

      cls.read_section_line( draft, raw_line, stripped )


   @classmethod
   def read_fixed_count( cls, draft: ReportDraft, stripped: str ) -> bool:
      fixed_count = cls.fixed_count( stripped )

      if fixed_count is None:
         return False

      draft.fixed_count = fixed_count
      return True


   @classmethod
   def read_counts( cls, draft: ReportDraft, stripped: str ) -> bool:
      if cls.count_line_re().match( stripped ) is None:
         return False

      draft.counts = cls.parse_counts( stripped )
      draft.finish_section()
      return True


   @classmethod
   def read_header( cls, draft: ReportDraft, stripped: str ) -> bool:
      header = cls.header_re().match( stripped )

      if header is None:
         return False

      note = header.group( 'note' ) or ''
      draft.start_section( header.group( 'kind' ), header.group( 'day' ), note )
      return True


   @classmethod
   def read_section_line( cls, draft: ReportDraft, raw_line: str, stripped: str ) -> None:
      if draft.current is None or stripped == '':
         return

      if cls.read_category( draft, raw_line ):
         return

      cls.read_entry( draft, raw_line, stripped )


   @classmethod
   def read_category( cls, draft: ReportDraft, raw_line: str ) -> bool:
      category_match = cls.CATEGORY_RE.match( raw_line )

      if category_match is None:
         return False

      draft.start_category(
         category_match.group( 'title' ),
         int( category_match.group( 'count' ) ),
      )
      return True


   @classmethod
   def read_entry( cls, draft: ReportDraft, raw_line: str, stripped: str ) -> None:
      if draft.category is None:
         draft.add_note( stripped )
         return

      if raw_line.startswith( CheckReport.detail_prefix() ):
         draft.add_detail( stripped )
         return

      draft.add_item( stripped )
