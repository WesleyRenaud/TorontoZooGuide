from __future__ import annotations

import re

from api.shared.enums.item_type import ItemType
from api.shared.text_values import TextValues
from .temporary_closure import TemporaryClosure
from .viewing_alert_sentence_builder import ViewingAlertSentenceBuilder
from .website_closure import WebsiteClosure


class TemporaryClosureReader():
   SKIP_RE = re.compile( r'\b(?:nearest|alternate)\b|remain open', re.I )
   PLACE_RE = re.compile( r'\b(?:station|restrooms?|washrooms?|bathrooms?)\b', re.I )
   WEEKDAY_RE = re.compile( r'\bweekdays\b|monday to friday', re.I )
   CLOSED_RE = re.compile( r'\b(?:close|closed|closing|closure|unavailable)\b', re.I )
   FOLDS = str.maketrans( {
      'á': 'a',
      'é': 'e',
      'è': 'e',
      'ê': 'e',
      '’': "'",
   } )


   @classmethod
   def fold( cls, value: str ) -> str:
      return value.casefold().translate( cls.FOLDS )


   @classmethod
   def text( cls, notice: WebsiteClosure ) -> str:
      title = notice.title.strip()

      if title != '' and title[ -1 ] not in '.!?':
         title = f'{ title }.'

      return TextValues.beside( title, notice.description )


   @classmethod
   def closure( cls, sentence: str ) -> bool:
      folded = sentence.casefold()
      return (
         cls.SKIP_RE.search( folded ) == None
         and WebsiteClosure.SEASON_RE.search( folded ) == None
         and cls.WEEKDAY_RE.search( folded ) == None
         and cls.CLOSED_RE.search( folded ) != None
      )


   @classmethod
   def index( cls, folded: str, needle: str ) -> int | None:
      if needle == '':
         return None

      for match in re.finditer( rf'(?<!\w){ re.escape( needle ) }(?!\w)', folded ):
         if cls.PLACE_RE.match( folded[ match.end() : ].lstrip() ) == None:
            return match.start()

      return None


   @classmethod
   def mentioned( cls, sentence: str, names: list[ str ] ) -> list[ str ]:
      folded = cls.fold( sentence )
      found = []

      for name in sorted( names, key=lambda name: len( cls.fold( name ) ), reverse=True ):
         needle = cls.fold( name )
         index = cls.index( folded, needle )

         if index == None:
            continue

         found.append( name )
         folded = folded[ : index ] + ( ' ' * len( needle ) ) + folded[ index + len( needle ) : ]

      return found


   @classmethod
   def read(
         cls,
         page_html: str,
         photo_paths: dict[ str, str ],
         kind: ItemType ) -> list[ TemporaryClosure ]:
      found = {}

      for notice in WebsiteClosure.notices( page_html ):
         for sentence in ViewingAlertSentenceBuilder.notice_parts( cls.text( notice ) ):
            if not cls.closure( sentence ):
               continue

            for name in cls.mentioned( sentence, list( photo_paths ) ):
               key = ( name, sentence )

               if key in found:
                  continue

               found[ key ] = TemporaryClosure(
                  name,
                  sentence,
                  kind,
                  photo_paths[ name ],
               )

      return list( found.values() )
