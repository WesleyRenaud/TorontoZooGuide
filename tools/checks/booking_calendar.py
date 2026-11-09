from __future__ import annotations

from datetime import date
from datetime import timedelta
import json
import re
import subprocess

from api.app_string_provider import AppStringProvider


class BookingCalendar():
   GRAPHQL_URL = 'https://my.hornblower.com/graphql'
   PROPERTY_ID = 'tozoo'
   USER_AGENT = 'Mozilla/5.0'
   TOUR_ID_RE = re.compile( r'tour-id=["\'](?P<id>\d+)["\']' )
   ENABLED_DATES_QUERY = """
      query enabledDates(
         $propertyId: String!,
         $bookingType: String!,
         $correlationId: String!,
         $startDate: String!,
         $endDate: String! ) {
         enabledDates(
            propertyId: $propertyId,
            bookingType: $bookingType,
            correlationId: $correlationId,
            startDate: $startDate,
            endDate: $endDate ) {
            year
            months {
               month
               days
            }
         }
      }
   """


   @classmethod
   def curl( cls, args: list[ str ], body: str | None = None ) -> str:
      result = subprocess.run(
         [
            'curl',
            '-fsS',
            '--max-time',
            '30',
            '-A',
            cls.USER_AGENT,
            *args,
         ],
         input=None if body == None else body.encode(),
         check=False,
         capture_output=True,
      )

      if result.returncode != 0:
         detail = result.stderr.decode( errors='replace' ).strip()
         raise RuntimeError( detail or AppStringProvider.format( 'checks.curlExited' ) )

      return result.stdout.decode()


   @classmethod
   def post_json( cls, url: str, payload: dict[ str, object ] ) -> dict[ str, object ]:
      return json.loads( cls.curl(
         [
            '-H',
            'Content-Type: application/json',
            '--data-binary',
            '@-',
            url,
         ],
         json.dumps( payload ),
      ) )


   @classmethod
   def tour_id( cls, page_html: str ) -> str | None:
      match = cls.TOUR_ID_RE.search( page_html )

      if match == None:
         return None

      return match.group( 'id' )


   @classmethod
   def enabled_dates_from( cls, booking_type: str, first: date ) -> list[ date ]:
      found: list[ date ] = []
      cursor = first

      while True:
         chunk_last = cursor + timedelta( days=365 )
         chunk = cls.enabled_dates( booking_type, cursor, chunk_last )

         if chunk == []:
            return found

         found.extend( chunk )
         cursor = chunk_last + timedelta( days=1 )


   @classmethod
   def enabled_dates( cls, booking_type: str, first: date, last: date ) -> list[ date ]:
      scheduled_dates = cls.calendar_dates( cls.enabled_date_rows( booking_type, first, last ) )
      return [
         scheduled_date
         for scheduled_date in scheduled_dates
         if first <= scheduled_date <= last
      ]


   @classmethod
   def enabled_date_rows(
         cls,
         booking_type: str,
         first: date,
         last: date ) -> list[ dict[ str, object ] ]:
      payload = cls.post_json(
         cls.GRAPHQL_URL,
         {
            'query': cls.ENABLED_DATES_QUERY,
            'variables': {
               'propertyId': cls.PROPERTY_ID,
               'bookingType': booking_type,
               'correlationId': 'tzg-schedule-check',
               'startDate': first.strftime( '%m/%d/%Y' ),
               'endDate': last.strftime( '%m/%d/%Y' ),
            },
         },
      )
      errors = payload.get( 'errors' )

      if errors:
         raise RuntimeError( str( errors[ 0 ][ 'message' ] ) )

      return payload[ 'data' ][ 'enabledDates' ]


   @classmethod
   def calendar_dates( cls, year_rows: list[ dict[ str, object ] ] ) -> list[ date ]:
      return [
         date(
            cls.calendar_year( int( year_row[ 'year' ] ) ),
            int( month_row[ 'month' ] ),
            int( day ),
         )
         for year_row in year_rows
         for month_row in year_row[ 'months' ]
         for day in month_row[ 'days' ]
      ]


   @classmethod
   def calendar_year( cls, year: int ) -> int:
      if year < 100:
         return year + 2000

      return year
