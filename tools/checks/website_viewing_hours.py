from __future__ import annotations

import re

from .animal_catalogue import AnimalCatalogue
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.shared.date_values import DateValues
from .exhibit_name import ExhibitName
from .viewing_hours import ViewingHours
from .website_page import WebsitePage


class WebsiteViewingHours():
   DAILY_FROM_RE = re.compile(
      r'(?is)\bdaily from\s+'
      r'(?P<start>\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?))'
      r'\s*(?:-|–|to)\s*'
      r'(?P<end>\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?))'
   )
   ANIMAL_LINK_RE = re.compile( r'(?is)href="[^"]*?/animals/([^"?#]+)"' )
   HEADING_RE = re.compile( r'(?is)<h[1-3]\b[^>]*>(?P<body>.*?)</h[1-3]>' )
   STYLE_RE = re.compile( r'(?is)<(script|style)\b[^>]*>.*?</\1>' )
   INDIVIDUAL_RE = re.compile(
      r'(?i:\b(baby|calf|pups?|joeys?|cubs?))\s+([A-Z][A-Za-z]+)'
   )


   @classmethod
   def clock( cls, value: str ) -> str | None:
      try:
         return DateValues.format_display_time_value( re.sub( r'[\s.]', '', value ).upper() )
      except ValueError:
         return None


   @classmethod
   def names_species(
         cls,
         page_html: str,
         page_path: str,
         sentence: str,
         placements: list[ AnimalSpeciesExhibit ] ) -> set[ str ]:
      names = [ sentence ]

      for heading in cls.HEADING_RE.finditer( page_html ):
         names.append( WebsitePage.clean_html( heading.group( 'body' ) ) )

      for tail in cls.ANIMAL_LINK_RE.findall( page_html ):
         names.append( WebsitePage.clean_website_name( tail ) )

      path = page_path.strip( '/' )

      if path.casefold().startswith( 'animals/' ):
         names.append( WebsitePage.clean_website_name( path.split( '/', 1 )[ 1 ] ) )

      text = f' { WebsitePage.normalize_name( " ".join( names ) ) } '
      named: set[ str ] = set()

      for placement in placements:
         key = AnimalCatalogue.comparison_key( placement.species, False )

         if key != '' and f' { key } ' in text:
            named.add( placement.species )

      return named


   @classmethod
   def subject( cls, text: str, sentence_end: int, species: str ) -> str:
      note_end = text.find( '.', sentence_end + 1 )

      if note_end < 0:
         note_end = len( text )

      found = cls.INDIVIDUAL_RE.findall( text[ sentence_end:note_end ] )

      if len( found ) != 1:
         return species

      return f'{ found[ 0 ][ 0 ].casefold() } { species.casefold() } { found[ 0 ][ 1 ] }'


   @classmethod
   def schedules(
         cls,
         page_html: str,
         page_path: str,
         placements: list[ AnimalSpeciesExhibit ] ) -> list[ ViewingHours ]:
      text = WebsitePage.clean_html( cls.STYLE_RE.sub( ' ', page_html ) )
      match = cls.DAILY_FROM_RE.search( text )

      if match == None:
         return []

      opens = cls.clock( match.group( 'start' ) )
      closes = cls.clock( match.group( 'end' ) )

      if opens == None or closes == None:
         return []

      end = text.find( '.', match.end() )

      if end < 0:
         end = len( text )

      sentence = text[ match.start():end ]
      named = cls.names_species( page_html, page_path, sentence, placements )
      sentence_key = ExhibitName.key( sentence )
      found = []

      for placement in placements:
         exhibit_key = ExhibitName.key( placement.exhibit )

         if exhibit_key == '' or exhibit_key not in sentence_key or placement.species not in named:
            continue

         found.append( ViewingHours(
            placement.species,
            placement.exhibit,
            None,
            None,
            opens,
            closes,
            cls.subject( text, end, placement.species ),
         ) )

      return found
