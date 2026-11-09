from __future__ import annotations

import json
from pathlib import Path
import re

from api.app_string_provider import AppStringProvider
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.domain.attraction_info_link import AttractionInfoLink
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from .attraction_card import AttractionCard
from .attraction_detail_image import AttractionDetailImage
from .attraction_listing import AttractionListing
from .check_report import CheckReport
from .paths import Paths
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage


class AttractionCatalogue():
   CARD_IMAGE_RE = re.compile( r'(?is)<img\b[^>]*\bsrc="(?P<src>[^"]+)"' )


   @classmethod
   def card_image( cls, body: str ) -> str:
      match = cls.CARD_IMAGE_RE.search( body )

      if match == None:
         return ''

      return WebsitePage.absolute_url( match.group( 'src' ) )


   @classmethod
   def website_attractions( cls, cards: list[ AttractionCard ] ) -> list[ WebsiteAttraction ]:
      return [
         WebsiteAttraction(
            href=card.href,
            title=WebsitePage.col3_title( card.body ),
            status=WebsitePage.opening_status( card.body ),
            image=cls.card_image( card.body ),
         )
         for card in cards
      ]


   @classmethod
   def parse_website_attractions( cls, page_html: str ) -> list[ WebsiteAttraction ]:
      return cls.website_attractions( AttractionCard.find( page_html ) )


   @classmethod
   def fetch_website_attractions( cls ) -> list[ WebsiteAttraction ]:
      return cls.parse_website_attractions(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ATTRACTIONS ) )
      )


   @classmethod
   def load_attractions( cls, database: Path ) -> list[ AttractionInfoLink ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AttractionCoordinator.get_attraction_info_links()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def app_listings( cls, attractions: list[ AttractionInfoLink ] ) -> list[ AttractionListing ]:
      return [
         AttractionListing( name=attraction.name, link=attraction.info_link )
         for attraction in attractions
      ]


   @classmethod
   def website_listings( cls, attractions: list[ WebsiteAttraction ] ) -> list[ AttractionListing ]:
      return [
         AttractionListing(
            name=attraction.title,
            link=attraction.href,
            image=attraction.image,
         )
         for attraction in attractions
         if not AttractionListing( name=attraction.title ).is_website_only()
      ]


   @classmethod
   def seed_region( cls, name: str ) -> str | None:
      folded = name.casefold()

      for row in json.loads( Paths.ATTRACTION_DATA.read_text() ):
         if row[ 'name' ].casefold() == folded:
            return row[ 'region' ]

      return None


   @classmethod
   def app_photo( cls, name: str ) -> str:
      photo = AttractionDetailImage.source( name )

      if ( Paths.ROOT / photo ).is_file():
         return photo

      return ''


   @classmethod
   def photo_line( cls, title: str, photo: str ) -> str:
      if photo == '':
         return title

      return CheckReport.join_lines( [
         title,
         CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo ),
      ] )


   @classmethod
   def app_line( cls, name: str ) -> str:
      region = cls.seed_region( name )

      if region == None:
         return name

      return cls.photo_line(
         AppStringProvider.format(
            'format.middleDotPair',
            first=name,
            second=region,
         ),
         cls.app_photo( name ),
      )


   @classmethod
   def website_line( cls, listing: AttractionListing ) -> str:
      return cls.photo_line( listing.name, listing.image )


   @classmethod
   def missing_listings(
         cls,
         source: list[ AttractionListing ],
         other: list[ AttractionListing ] ) -> list[ AttractionListing ]:
      missed: dict[ str, AttractionListing ] = {}

      for listing in source:
         if any( listing.matches( candidate ) for candidate in other ):
            continue

         missed.setdefault( WebsitePage.normalize_name( listing.name ), listing )

      return sorted( missed.values(), key=cls.listing_name )


   @classmethod
   def listing_name( cls, listing: AttractionListing ) -> str:
      return listing.name.casefold()


   @classmethod
   def missing_names(
         cls,
         source: list[ AttractionListing ],
         other: list[ AttractionListing ] ) -> list[ str ]:
      return [
         listing.name
         for listing in cls.missing_listings( source, other )
      ]
