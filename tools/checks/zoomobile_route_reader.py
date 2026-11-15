from __future__ import annotations

import re

from api.app_string_provider import AppStringProvider
from api.shared.enums.transportation_route_id import TransportationRouteId
from .booking_calendar import BookingCalendar
from .check_report import CheckReport
from .website_page import WebsitePage
from .zoomobile_route import ZoomobileRoute


class ZoomobileRouteReader():
   ROUTE_RE = re.compile(
      rf'operating on its (?P<route>{ TransportationRouteId.SUMMER.value }|{ TransportationRouteId.WINTER.value }) route',
      re.I,
   )
   SUMMER_RE = re.compile( r'canadian domain|african savanna|africa savanna', re.I )
   ITEM_RE = re.compile( r'(?is)<li>(.*?)</li>' )


   @classmethod
   def description( cls, booking_type: str ) -> str:
      payload = BookingCalendar.post_json(
         BookingCalendar.GRAPHQL_URL,
         {
            'query': BookingCalendar.SEARCH_TOURS_QUERY,
            'variables': {
               'propertyId': BookingCalendar.PROPERTY_ID,
               'bookingType': booking_type,
            },
         },
      )
      values = []

      for tour in payload[ 'data' ][ 'searchTours' ]:
         for info in tour.get( 'localizedInfo' ) or []:
            if info.get( 'locale' ) != 'en':
               continue

            values.extend(
               item[ 'value' ]
               for item in info.get( 'values' ) or []
               if item.get( 'value' )
            )

      return CheckReport.join_lines( values )


   @classmethod
   def stations( cls, description: str ) -> list[ str ]:
      return [
         item
         for item in map( WebsitePage.clean_html, cls.ITEM_RE.findall( description ) )
         if item != ''
      ]


   @classmethod
   def parse( cls, description: str ) -> ZoomobileRoute | None:
      stations = cls.stations( description )
      named = cls.ROUTE_RE.search( description )

      if named == None and stations == []:
         return None

      route = TransportationRouteId.WINTER.value

      if named != None:
         route = named.group( 'route' ).casefold()
      elif cls.SUMMER_RE.search( ' '.join( stations ) ) != None:
         route = TransportationRouteId.SUMMER.value

      return ZoomobileRoute( route )


   @classmethod
   def read( cls ) -> ZoomobileRoute:
      page = WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ZOOMOBILE ) )
      tour_id = BookingCalendar.tour_id( page )
      route = None if tour_id == None else cls.parse( cls.description( tour_id ) )

      if route == None:
         raise RuntimeError(
            AppStringProvider.format( 'checks.couldNotReadZoomobileRoute' )
         )

      return route
