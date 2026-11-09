from __future__ import annotations

from datetime import date

from api.app_string_provider import AppStringProvider
from .date_span import DateSpan


class CheckReport():
   fixed_count = 0


   @classmethod
   def reset_fixed_count( cls ) -> None:
      cls.fixed_count = 0


   @classmethod
   def note_fixed( cls, count: int ) -> None:
      cls.fixed_count += count


   @classmethod
   def text( cls, key: str ) -> str:
      return AppStringProvider.format( key )


   @classmethod
   def label( cls, key: str ) -> str:
      value = cls.text( key )
      separator = cls.text( 'checks.labelValue' )
      return value.removesuffix( separator )


   @classmethod
   def category_line( cls, key: str, count: int ) -> str:
      return f'{ cls.text( key ) }{ cls.text( "checks.labelValue" ) }{ count }'


   @classmethod
   def print_category(
         cls,
         key: str,
         items: list[ str ],
         indent: bool = True ) -> None:
      print( cls.category_line( key, len( items ) ) )

      for item in items:
         if indent:
            print( cls.text( 'checks.categoryItem' ) + item )
         else:
            print( item )

      print()


   @classmethod
   def report_differences(
         cls,
         heading: str,
         website_only: list[ str ],
         app_only: list[ str ] ) -> None:
      print( heading )
      print()
      cls.print_category( 'checks.websiteOnly', website_only )
      cls.print_category( 'checks.appOnly', app_only )


   @classmethod
   def count_differences(
         cls,
         website_only: list[ str ],
         app_only: list[ str ] ) -> int:
      return len( website_only ) + len( app_only )


   @classmethod
   def report_category(
         cls,
         check: str,
         day: date,
         note: str,
         key: str,
         items: list[ str ] ) -> None:
      print( f'{ cls.heading( check, day ) } { note }' )
      print()
      cls.print_category( key, items, indent=False )


   @classmethod
   def heading( cls, check: str, day: date ) -> str:
      return (
         AppStringProvider.reports()[ check ][ 'kind' ]
         + cls.text( 'checks.headingMiddle' )
         + day.isoformat()
         + cls.text( 'checks.period' )
      )


   @classmethod
   def join_lines( cls, lines: list[ str ] ) -> str:
      return '\n'.join( lines )


   @classmethod
   def detail_item( cls, item: str ) -> str:
      return cls.text( 'checks.detailItem' ) + item


   @classmethod
   def detail_prefix( cls ) -> str:
      return cls.detail_item( '' )


   @classmethod
   def format_date_span( cls, start: date, end: date ) -> str:
      if start == end:
         return start.isoformat()

      return start.isoformat() + cls.text( 'checks.dateThrough' ) + end.isoformat()


   @classmethod
   def date_spans( cls, dates: list[ date ] ) -> list[ DateSpan ]:
      ordered = sorted( dates )
      spans = [ DateSpan( start=ordered[ 0 ], end=ordered[ 0 ] ) ]

      for current in ordered[ 1: ]:
         if spans[ -1 ].is_next_day( current ):
            spans[ -1 ] = spans[ -1 ].extended_to( current )
            continue

         spans.append( DateSpan( start=current, end=current ) )

      return spans


   @classmethod
   def format_date_list( cls, dates: list[ date ] ) -> str:
      return AppStringProvider.values()[ 'format.listJoin' ].join(
         cls.format_date_span( span.start, span.end )
         for span in cls.date_spans( dates )
      )
