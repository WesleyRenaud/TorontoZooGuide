from __future__ import annotations

from datetime import date
from html import escape

from api.app_string_provider import AppStringProvider
from .category import Category
from .check_exit_code import CheckExitCode
from .check_report_parser import CheckReportParser
from .color_token import ColorToken
from .color_tokens import ColorTokens
from .count import Count
from .detail_item import DetailItem
from .email_template_renderer import EmailTemplateRenderer
from .exhibit_region_colors import ExhibitRegionColors
from .font_tokens import FontTokens
from .report import Report
from .section import Section
from .status_copy import StatusCopy


class CheckEmailRenderer():
   @classmethod
   def markup( cls, name: str, **params: object ) -> str:
      values: dict[ str, object ] = {
         'font': FontTokens.font( 'font-family-email' ),
         'green': ColorTokens.color( ColorToken.BRAND_PRIMARY ),
         'green_dark': ColorTokens.color( ColorToken.BRAND_PRIMARY_DARK ),
         'green_muted': ColorTokens.color( ColorToken.BRAND_PRIMARY_MUTED ),
         'green_highlight': ColorTokens.color( ColorToken.BRAND_ACCENT ),
         'leaf_edge': ColorTokens.color( ColorToken.BORDER_LEAF ),
         'text': ColorTokens.color( ColorToken.TEXT_PRIMARY ),
         'panel': ColorTokens.color( ColorToken.SURFACE_PANEL ),
         'white': ColorTokens.color( ColorToken.WHITE ),
         'danger': ColorTokens.color( ColorToken.DANGER ),
         'danger_soft': ColorTokens.color( ColorToken.DANGER_SOFT ),
      }
      values.update( params )
      return EmailTemplateRenderer.render( name, **values )


   @classmethod
   def check_kind( cls, check: str ) -> str:
      return AppStringProvider.reports()[ check ][ 'kind' ]


   @classmethod
   def section_name( cls, kind: str ) -> str:
      titles = {
         report[ 'kind' ]: report.get( 'section', report[ 'kind' ] )
         for report in AppStringProvider.reports().values()
         if 'kind' in report
      }
      return titles.get( kind, kind )


   @classmethod
   def format_day( cls, day: str ) -> str:
      parsed = date.fromisoformat( day )
      return f'{ parsed.strftime( "%A" ) }, { parsed.strftime( "%B" ) } { parsed.day }, { parsed.year }'


   @classmethod
   def text( cls, value: str ) -> str:
      return escape( value, quote=True )


   @classmethod
   def status_copy( cls, exit_code: int, error_count: int | None ) -> StatusCopy:
      if exit_code == CheckExitCode.COULD_NOT_FINISH or error_count is None:
         return StatusCopy(
            headline_color=ColorTokens.color( ColorToken.DANGER ),
            headline=AppStringProvider.format( 'checks.status.couldNotFinish' ),
            summary=AppStringProvider.format( 'checks.status.didNotFinish' ),
         )

      if error_count == 0:
         return StatusCopy(
            headline_color=ColorTokens.color( ColorToken.BRAND_PRIMARY ),
            headline=AppStringProvider.format( 'checks.status.allClear' ),
            summary=AppStringProvider.format( 'checks.status.websiteMatches' ),
         )

      return StatusCopy(
         headline_color=ColorTokens.color( ColorToken.DANGER ),
         headline=CheckReportParser.format_error_count( error_count ),
         summary=AppStringProvider.format( 'checks.status.differ' ),
      )


   @classmethod
   def count_cell( cls, label: str, count: int ) -> str:
      clear = count == 0
      return cls.markup(
         'count_cell',
         label=cls.text( label ),
         count=cls.text( str( count ) ),
         number_color=(
            ColorTokens.color( ColorToken.BRAND_PRIMARY )
            if clear
            else ColorTokens.color( ColorToken.DANGER )
         ),
         background=(
            ColorTokens.color( ColorToken.WHITE )
            if clear
            else ColorTokens.color( ColorToken.DANGER_SOFT )
         ),
         edge=(
            ColorTokens.color( ColorToken.BORDER_LEAF )
            if clear
            else ColorTokens.color( ColorToken.DANGER )
         ),
      )


   @classmethod
   def count_row( cls, counts: list[ Count ] ) -> str:
      cells = ''.join(
         cls.count_cell( count.label, count.count )
         for count in counts
      )

      if len( counts ) < 2:
         cells += cls.markup( 'blank_count_cell' )

      return cls.markup( 'row', cells=cells )


   @classmethod
   def count_grid( cls, counts: list[ Count ] ) -> str:
      rows = []
      row: list[ Count ] = []

      for count in counts:
         row.append( count )

         if len( row ) < 2:
            continue

         rows.append( cls.count_row( row ) )
         row = []

      if row:
         rows.append( cls.count_row( row ) )

      return cls.markup( 'count_grid', rows=''.join( rows ) )


   @classmethod
   def detail_text( cls, detail: str ) -> str:
      label, separator, value = detail.partition( ': ' )

      if not separator:
         return cls.text( detail )

      return cls.markup(
         'detail_label',
         label=cls.text( label ),
         separator=separator,
         value=cls.text( value ),
      )


   @classmethod
   def exhibit_pill( cls, exhibit: str ) -> str:
      colors = ExhibitRegionColors.exhibit_colors( exhibit )
      safe = cls.text( exhibit )
      return cls.markup(
         'exhibit_pill',
         exhibit=safe,
         background=colors.background,
         foreground=colors.foreground,
      )


   @classmethod
   def item_label( cls, title: str ) -> str:
      species, separator, exhibit = title.rpartition( ' · ' )

      if separator == '':
         return cls.text( title )

      return f'{ cls.text( species ) }{ separator }{ cls.exhibit_pill( exhibit ) }'


   @classmethod
   def detail_rows( cls, item: DetailItem ) -> str:
      rows = [
         cls.markup(
            'row',
            cells=cls.markup( 'item_title', label=cls.item_label( item.title ) ),
         )
      ]

      for detail in item.details:
         rows.append(
            cls.markup(
               'row',
               cells=cls.markup( 'detail_line', detail=cls.detail_text( detail ) ),
            )
         )

      return ''.join( rows )


   @classmethod
   def category_block( cls, category: Category ) -> str:
      number_color = (
         ColorTokens.color( ColorToken.BRAND_PRIMARY )
         if category.count == 0
         else ColorTokens.color( ColorToken.DANGER )
      )
      title_cell = cls.markup( 'category_title', title=cls.text( category.title ) )
      count_badge = cls.markup(
         'category_count',
         number_color=number_color,
         count=cls.text( str( category.count ) ),
      )
      rows = [ cls.markup( 'row', cells=title_cell + count_badge ) ]
      rows.extend( cls.detail_rows( item ) for item in category.items )
      return ''.join( rows )


   @classmethod
   def section_card( cls, section: Section ) -> str:
      title = cls.markup(
         'section_title',
         title=cls.text( cls.section_name( section.kind ) ),
      )
      rows = [ cls.markup( 'row', cells=title ) ]

      if section.categories:
         rows.append(
            cls.markup(
               'section_categories',
               categories=''.join(
                  cls.category_block( category )
                  for category in section.categories
               ),
            )
         )

      return cls.markup( 'section_card', rows=''.join( rows ) )


   @classmethod
   def animal_sections( cls, sections: list[ Section ] ) -> list[ Section ]:
      kinds = (
         cls.check_kind( 'animalList' ),
         cls.check_kind( 'seasonalOffDisplay' ),
      )
      by_kind = {
         section.kind: section
         for section in sections
         if section.kind in kinds
      }
      return [
         by_kind[ kind ]
         for kind in kinds
         if kind in by_kind
      ]


   @classmethod
   def has_issue( cls, categories: list[ Category ] ) -> bool:
      return any( category.count > 0 for category in categories )


   @classmethod
   def combined_animals( cls, sections: list[ Section ] ) -> Section | None:
      sources = cls.animal_sections( sections )
      categories = [
         category
         for section in sources
         for category in section.categories
      ]

      if not cls.has_issue( categories ):
         return None

      return Section( AppStringProvider.format( 'site.nav.animals' ), sources[ 0 ].day, '', categories )


   @classmethod
   def notable_sections( cls, report: Report ) -> list[ Section ]:
      notable = []
      animals = cls.combined_animals( report.sections )
      animals_placed = False
      folded = {
         section.kind
         for section in cls.animal_sections( report.sections )
      }

      for section in report.sections:
         if section.kind in folded:
            if animals is not None and not animals_placed:
               notable.append( animals )
               animals_placed = True

            continue

         if cls.has_issue( section.categories ):
            notable.append( section )

      return notable


   @classmethod
   def render_html( cls, body: str, exit_code: int ) -> str:
      report = CheckReportParser.parse_report( body )
      day = report.sections[ 0 ].day
      status = cls.status_copy( exit_code, report.error_count )
      date_line = cls.markup( 'date_line', day=cls.text( cls.format_day( day ) ) )
      sections = cls.notable_sections( report )
      detail = ''.join( cls.section_card( section ) for section in sections )
      content = (
         cls.markup( 'header', title_padding='6px 24px 2px', date_line=date_line )
         + cls.markup(
            'status',
            headline_color=status.headline_color,
            headline=cls.text( status.headline ),
            summary=cls.text( status.summary ),
         )
         + cls.count_grid( report.counts )
         + detail
      )
      return cls.markup( 'document', content=content )
