from __future__ import annotations

from dataclasses import dataclass
from html import unescape
from urllib.parse import unquote

from .animal_catalogue import AnimalCatalogue
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.app_string_provider import AppStringProvider
from .website_off_display_animal import WebsiteOffDisplayAnimal
from .website_page import WebsitePage


@dataclass( frozen=True )
class WebsiteTemporarilyOffDisplayAnimal:
   section: str
   name: str


   def matches( self, enclosure: AnimalSpeciesExhibit ) -> bool:
      return (
         WebsitePage.normalize_name( self.section ) == WebsitePage.normalize_name( enclosure.exhibit )
         and AnimalCatalogue.same_name( self.name, enclosure.species )
      )


   @classmethod
   def from_page( cls, page_html: str ) -> list[ WebsiteTemporarilyOffDisplayAnimal ]:
      animals = []

      for section in WebsiteOffDisplayAnimal.SECTION_RE.finditer( page_html ):
         animals.extend( cls.animals_in_section(
            unescape( unquote( section.group( 'id' ) ) ).strip(),
            section.group( 'body' ),
         ) )

      return animals


   @classmethod
   def animals_in_section(
         cls,
         section: str,
         body: str ) -> list[ WebsiteTemporarilyOffDisplayAnimal ]:
      animals = []
      phrase = AppStringProvider.format( 'checks.temporarilyNotViewable' )

      for href, card in WebsiteOffDisplayAnimal.ANIMAL_RE.findall( body ):
         if 'status notviewable' not in card.casefold():
            continue

         if phrase not in WebsitePage.clean_html( card ).casefold():
            continue

         animals.append( cls(
            section=section,
            name=WebsitePage.clean_website_name( href ),
         ) )

      return animals


   @classmethod
   def fetch( cls ) -> list[ WebsiteTemporarilyOffDisplayAnimal ]:
      return cls.from_page(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) )
      )
