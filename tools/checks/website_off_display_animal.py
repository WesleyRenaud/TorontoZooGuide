from __future__ import annotations

from dataclasses import dataclass
from html import unescape
import re
from typing import ClassVar
from urllib.parse import unquote

from api.app_string_provider import AppStringProvider
from .website_page import WebsitePage


@dataclass( frozen=True )
class WebsiteOffDisplayAnimal:
   SECTION_RE: ClassVar[ re.Pattern[ str ] ] = re.compile(
      r'(?is)<div class="atitle[^"]*" id="(?P<id>[^"]+)">(?P<body>.*?)(?=<div class="atitle|\Z)',
   )
   ANIMAL_RE: ClassVar[ re.Pattern[ str ] ] = re.compile(
      r'(?is)<a href="/animals/([^"]+)"(.*?)</a>',
   )
   section: str
   name: str


   @classmethod
   def from_page( cls, page_html: str ) -> list[ WebsiteOffDisplayAnimal ]:
      animals = []

      for section in cls.SECTION_RE.finditer( page_html ):
         animals.extend( cls.animals_in_section(
            unescape( unquote( section.group( 'id' ) ) ).strip(),
            section.group( 'body' ),
         ) )

      return animals


   @classmethod
   def animals_in_section( cls, section: str, body: str ) -> list[ WebsiteOffDisplayAnimal ]:
      animals = []

      for href, card in cls.ANIMAL_RE.findall( body ):
         if 'status sseason' not in card.casefold():
            continue

         if AppStringProvider.format( 'checks.offForSeason' ) not in WebsitePage.clean_html( card ).casefold():
            continue

         animals.append( cls(
            section=section,
            name=WebsitePage.clean_website_name( href ),
         ) )

      return animals


   @classmethod
   def fetch( cls ) -> list[ WebsiteOffDisplayAnimal ]:
      return cls.from_page(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) )
      )
