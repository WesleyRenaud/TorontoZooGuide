from __future__ import annotations

from html import unescape
from pathlib import Path
import re

from .animal_detail_image import AnimalDetailImage
from .animal_listing import AnimalListing
from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from .check_report import CheckReport
from .paths import Paths
from .website_page import WebsitePage


class AnimalCatalogue():
   PAGE = 'animals'
   WEBSITE_REGION_PATHS = (
      'africa',
      'americas',
      'australasia',
      'canada',
      'discovery',
      'eurasia',
      'indo-malaya',
      'tundra',
   )
   WEBSITE_NAME_ALIASES = {
      'wood bison female herd': 'wood bison',
      'wood bison male herd': 'wood bison',
   }
   HEADING_RE = re.compile( r'(?is)<h1\b[^>]*>(?P<title>.*?)</h1>' )
   ANIMAL_LINK_RE = re.compile( r'(?is)<a href="/animals/(?P<name>[^"]+)" class="thm"' )


   @classmethod
   def comparison_key( cls, name: str, use_website_aliases: bool ) -> str:
      normalized = WebsitePage.normalize_name( name )

      if use_website_aliases:
         return cls.WEBSITE_NAME_ALIASES.get( normalized, normalized )

      return normalized


   @classmethod
   def parse_website_animals( cls, page_html: str ) -> list[ AnimalSpeciesExhibit ]:
      names = []
      headings = list( cls.HEADING_RE.finditer( page_html ) )
      next_headings = headings[ 1: ]
      next_headings.append( None )

      for heading, next_heading in zip( headings, next_headings ):
         if next_heading == None:
            end = len( page_html )
         else:
            end = next_heading.start()

         exhibit = unescape( re.sub( r'<[^>]+>', ' ', heading.group( 'title' ) ) )
         exhibit = re.sub( r'\s+', ' ', exhibit ).strip()

         for href in cls.ANIMAL_LINK_RE.findall( page_html[ heading.end():end ] ):
            name = WebsitePage.clean_website_name( href )
            listing = AnimalSpeciesExhibit( species=name, exhibit=exhibit )

            if name == '' or listing in names:
               continue

            names.append( listing )

      return names


   @classmethod
   def fetch_website_animals( cls ) -> list[ AnimalSpeciesExhibit ]:
      animals = []

      for path in cls.WEBSITE_REGION_PATHS:
         page = WebsitePage.fetch_text( WebsitePage.url( f'{ cls.PAGE }/{ path }' ) )
         animals.extend( cls.parse_website_animals( page ) )

      return animals


   @classmethod
   def load_species( cls, database: Path ) -> list[ AnimalSpeciesExhibit ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AnimalCoordinator.get_animal_species_exhibits()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def listing_key(
         cls,
         exhibit: str,
         name: str,
         use_website_aliases: bool ) -> SpeciesExhibitKey:
      return SpeciesExhibitKey(
         species=cls.comparison_key( name, use_website_aliases ),
         exhibit=exhibit,
      )


   @classmethod
   def add_listing(
         cls,
         listings: dict[ SpeciesExhibitKey, AnimalListing ],
         exhibit: str,
         name: str,
         use_website_aliases: bool ) -> None:
      key = cls.listing_key( exhibit, name, use_website_aliases )
      stored = listings.get( key )

      if stored == None:
         listings[ key ] = AnimalListing( exhibit=exhibit, species=[ name ] )
         return

      if name not in stored.species:
         stored.species.append( name )


   @classmethod
   def listing_label( cls, species: list[ str ] ) -> str:
      return ' / '.join( sorted( species, key=str.casefold ) )


   @classmethod
   def app_photo( cls, key: SpeciesExhibitKey ) -> str:
      photo = AnimalDetailImage.source( key.exhibit, key.species )

      if ( Paths.ROOT / photo ).is_file():
         return photo

      return ''


   @classmethod
   def missing_labels(
         cls,
         source: dict[ SpeciesExhibitKey, AnimalListing ],
         other: dict[ SpeciesExhibitKey, AnimalListing ] ) -> list[ str ]:
      labels = []

      for key, listing in source.items():
         if key in other:
            continue

         label = AppStringProvider.format(
            'format.middleDotPair',
            first=cls.listing_label( listing.species ),
            second=listing.exhibit,
         )
         photo = cls.app_photo( key )

         if photo != '':
            label += '\n' + CheckReport.detail_item(
               CheckReport.text( 'checks.photo' ) + photo
            )

         labels.append( label )

      return sorted( labels, key=str.casefold )


   @classmethod
   def listings(
         cls,
         database: Path ) -> tuple[
            dict[ SpeciesExhibitKey, AnimalListing ],
            dict[ SpeciesExhibitKey, AnimalListing ],
         ]:
      app_listings: dict[ SpeciesExhibitKey, AnimalListing ] = {}
      website_listings: dict[ SpeciesExhibitKey, AnimalListing ] = {}

      for animal in cls.load_species( database ):
         cls.add_listing( app_listings, animal.exhibit, animal.species, False )

      for animal in cls.fetch_website_animals():
         cls.add_listing( website_listings, animal.exhibit, animal.species, True )

      return app_listings, website_listings
