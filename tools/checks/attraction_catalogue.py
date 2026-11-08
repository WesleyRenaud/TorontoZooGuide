from __future__ import annotations

from pathlib import Path

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.domain.attraction_info_link import AttractionInfoLink
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from .attraction_card import AttractionCard
from .attraction_listing import AttractionListing
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage


class AttractionCatalogue():
   @classmethod
   def website_attractions( cls, cards: list[ AttractionCard ] ) -> list[ WebsiteAttraction ]:
      return [
         WebsiteAttraction(
            href=card.href,
            title=WebsitePage.col3_title( card.body ),
            status=WebsitePage.opening_status( card.body ),
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
         AttractionListing( name=attraction.title, link=attraction.href )
         for attraction in attractions
         if not AttractionListing( name=attraction.title ).is_website_only()
      ]


   @classmethod
   def missing_names(
         cls,
         source: list[ AttractionListing ],
         other: list[ AttractionListing ] ) -> list[ str ]:
      names = {
         listing.name
         for listing in source
         if not any( listing.matches( candidate ) for candidate in other )
      }

      return sorted( names, key=str.casefold )
