from __future__ import annotations

from datetime import date
from pathlib import Path

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.domain.seasonal_attraction import SeasonalAttraction
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from .attraction_catalogue import AttractionCatalogue
from .attraction_listing import AttractionListing
from .website_attraction import WebsiteAttraction
from .website_page import WebsitePage


class SeasonalAttractionComparison():
   @classmethod
   def closed_for_season_attractions( cls, page_html: str, today: date ) -> list[ WebsiteAttraction ]:
      return [
         attraction
         for attraction in AttractionCatalogue.parse_website_attractions( page_html )
         if WebsitePage.is_closed_for_season_status( attraction.status, today )
      ]


   @classmethod
   def matched_attractions(
         cls,
         listing: WebsiteAttraction,
         attractions: list[ SeasonalAttraction ] ) -> list[ SeasonalAttraction ]:
      website = AttractionListing( name=listing.title, link=listing.href )

      return [
         attraction
         for attraction in attractions
         if AttractionListing( name=attraction.name, link=attraction.info_link ).matches( website )
      ]


   @classmethod
   def missed_website_attractions(
         cls,
         listings: list[ WebsiteAttraction ],
         attractions: list[ SeasonalAttraction ],
         today: date ) -> list[ str ]:
      return sorted(
         {
            attraction.name
            for listing in listings
            for attraction in cls.matched_attractions( listing, attractions )
            if not attraction.closed_for_season_on( today )
         },
         key=str.casefold,
      )


   @classmethod
   def missed_unmatched_listings(
         cls,
         listings: list[ WebsiteAttraction ],
         attractions: list[ SeasonalAttraction ] ) -> list[ str ]:
      return sorted(
         {
            listing.title
            for listing in listings
            if (
               not AttractionListing( name=listing.title ).is_website_only()
               and not cls.matched_attractions( listing, attractions )
            )
         },
         key=str.casefold,
      )


   @classmethod
   def website_attraction_names(
         cls,
         listings: list[ WebsiteAttraction ],
         attractions: list[ SeasonalAttraction ] ) -> set[ str ]:
      names: set[ str ] = set()

      for listing in listings:
         names.update(
            attraction.name
            for attraction in cls.matched_attractions( listing, attractions )
         )

      return names


   @classmethod
   def fetch_closed_for_season_attractions( cls, today: date ) -> list[ WebsiteAttraction ]:
      return cls.closed_for_season_attractions(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ATTRACTIONS ) ),
         today,
      )


   @classmethod
   def load_seasonal_attractions( cls, database: Path ) -> list[ SeasonalAttraction ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AttractionCoordinator.get_seasonal_attractions()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def app_only(
         cls,
         listings: list[ WebsiteAttraction ],
         attractions: list[ SeasonalAttraction ],
         today: date ) -> list[ str ]:
      names = cls.website_attraction_names( listings, attractions )

      return sorted(
         (
            attraction.name
            for attraction in attractions
            if attraction.closed_for_season_on( today ) and attraction.name not in names
         ),
         key=str.casefold,
      )
