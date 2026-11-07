from __future__ import annotations

from datetime import date

from api.app_string_provider import AppStringProvider
from .date_span import DateSpan
from .schedule_check import ScheduleCheck


class CheckReport():
   @classmethod
   def text( cls, key: str ) -> str:
      return AppStringProvider.format( key )


   @classmethod
   def print_category(
         cls,
         title: str,
         items: list[ str ],
         indent: bool = True ) -> None:
      print( f'{ title }{ cls.text( "checks.labelValue" ) }{ len( items ) }' )

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
      cls.print_category( AppStringProvider.format( 'checks.websiteOnly' ), website_only )
      cls.print_category( AppStringProvider.format( 'checks.appOnly' ), app_only )


   @classmethod
   def count_differences(
         cls,
         website_only: list[ str ],
         app_only: list[ str ] ) -> int:
      return len( website_only ) + len( app_only )


   @classmethod
   def report_schedule(
         cls,
         check: str,
         day: date,
         schedule: ScheduleCheck ) -> None:
      print( f'{ cls.heading( check, day ) } { schedule.note }' )
      print()
      cls.print_category(
         AppStringProvider.format( 'checks.scheduledInAppOnly' ),
         schedule.only_in_app,
         indent=False,
      )
      cls.print_category(
         AppStringProvider.format( 'checks.scheduledOnWebsiteOnly' ),
         schedule.only_on_website,
         indent=False,
      )
      cls.print_category(
         AppStringProvider.format( 'checks.differentDaysOrTimes' ),
         schedule.different_slots,
         indent=False,
      )
      cls.print_category(
         AppStringProvider.format( 'checks.windowsDoNotAlign' ),
         schedule.windows,
         indent=False,
      )


   @classmethod
   def count_schedule( cls, schedule: ScheduleCheck ) -> int:
      return (
         len( schedule.only_in_app )
         + len( schedule.only_on_website )
         + len( schedule.different_slots )
         + len( schedule.windows )
      )


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
